#!/usr/bin/env python3
"""Check supplied DOI/title/year metadata against Crossref; offline by default."""

import argparse
import csv
from datetime import datetime, timezone
import html
from http.client import HTTPException
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib import error, parse, request


API_BASE = "https://api.crossref.org/works/"
TIMEOUT_SECONDS = 15
REQUEST_INTERVAL_SECONDS = 1
MAX_ROWS = 500
STATUSES = (
    "not_checked_offline", "verified_metadata", "metadata_mismatch",
    "not_found", "network_error", "invalid_input",
)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_doi(value):
    value = value.strip()
    value = re.sub(r"^doi:\s*", "", value, flags=re.IGNORECASE)
    if re.match(r"^https?://(?:dx\.)?doi\.org/", value, re.IGNORECASE):
        value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value,
                       flags=re.IGNORECASE)
        value = parse.unquote(value)
    value = value.casefold()
    if not re.fullmatch(r"10\.\d{4,9}/\S+", value):
        raise ValueError("DOI must have the form 10.<4-9 digits>/<nonempty suffix>")
    if any(unicodedata.category(char).startswith("C") for char in value):
        raise ValueError("DOI contains a control or invisible formatting character")
    return value


def normalize_title(value):
    value = re.sub(r"</?(?:i|b|em|strong|sub|sup|span|jats:italic|jats:bold|jats:sub|jats:sup)\s*>",
                   "", value, flags=re.IGNORECASE)
    value = unicodedata.normalize("NFKC", html.unescape(value)).casefold()
    return " ".join("".join(f" {char} " if char in "<>≤≥=≠+-−±×÷" else
                            (char if char.isalnum() else " ") for char in value).split())


def publication_years(metadata):
    years = set()
    for field in ("published", "published-print", "published-online", "issued"):
        date = metadata.get(field)
        if not isinstance(date, dict):
            continue
        for parts in date.get("date-parts", []):
            if (isinstance(parts, list) and parts
                    and type(parts[0]) is int and 1000 <= parts[0] <= 9999):
                years.add(parts[0])
    return sorted(years)


def fetch_metadata(doi, transport):
    """One request, with no retry. A 404 means absent from Crossref only."""
    url = API_BASE + parse.quote(doi, safe="")
    checked_at = utc_now()
    req = request.Request(url, headers={
        "User-Agent": "FoodSciResearchAssistant/0.1 (bibliographic metadata check)",
        "Accept": "application/json",
    })
    result = {"evidence_url": url, "checked_at": checked_at,
              "retrieved": None, "stop_batch": False}
    try:
        with transport(req, timeout=TIMEOUT_SECONDS) as response:
            payload = json.load(response)
        metadata = payload.get("message") if isinstance(payload, dict) else None
        if not isinstance(metadata, dict):
            raise ValueError("Crossref response has no metadata object")
        titles = metadata.get("title", [])
        if not isinstance(titles, list) or not all(isinstance(t, str) for t in titles):
            raise ValueError("Crossref title field is not a list of strings")
        raw_doi = metadata.get("DOI", "")
        if not isinstance(raw_doi, str):
            raise ValueError("Crossref DOI field is not a string")
        result["retrieved"] = {"doi": raw_doi, "titles": titles,
                               "publication_years": publication_years(metadata)}
    except error.HTTPError as exc:
        result.update(status="not_found" if exc.code == 404 else "network_error",
                      reason=f"crossref_http_{exc.code}",
                      stop_batch=exc.code in (403, 429))
        exc.close()
    except (error.URLError, TimeoutError, OSError, HTTPException) as exc:
        result.update(status="network_error", reason=f"request_failed: {exc}")
    except (ValueError, TypeError) as exc:
        result.update(status="network_error", reason=f"unusable_crossref_response: {exc}")
    return result


def compare_metadata(record, retrieved):
    mismatches = []
    try:
        retrieved_doi = normalize_doi(retrieved["doi"])
    except ValueError:
        retrieved_doi = None
    if record["normalized_doi"] != retrieved_doi:
        mismatches.append("doi")
    expected = record["expected"]
    if normalize_title(expected["title"]) not in {
            normalize_title(title) for title in retrieved["titles"]}:
        mismatches.append("title")
    if int(expected["year"]) not in retrieved["publication_years"]:
        mismatches.append("year")
    return mismatches


def verify_rows(rows, online=False, transport=None, sleeper=None):
    """Rows are CSV dictionaries. Transport and sleeper are injectable for tests."""
    transport = transport or request.urlopen
    sleeper = sleeper or time.sleep
    records, cache = [], {}
    first_rows = {}
    stop_reason = None
    for number, row in enumerate(rows, start=2):
        expected = {key: (row.get(key) or "").strip() for key in ("doi", "title", "year")}
        record = {"row": number, "expected": expected, "normalized_doi": None,
                  "status": "invalid_input", "reason": None, "retrieved": None,
                  "mismatches": [], "evidence_url": None, "checked_at": None,
                  "duplicate_of_row": None}
        records.append(record)
        try:
            if None in row:
                raise ValueError("row has more fields than the CSV header")
            doi = normalize_doi(expected["doi"])
            record["normalized_doi"] = doi
            if not any(char.isalnum() for char in normalize_title(expected["title"])):
                raise ValueError("title must contain a letter or number")
            if not re.fullmatch(r"[1-9]\d{3}", expected["year"]):
                raise ValueError("year must be a four-digit integer (1000-9999)")
        except ValueError as exc:
            record["reason"] = str(exc)
            continue
        record["duplicate_of_row"] = first_rows.get(doi)
        first_rows.setdefault(doi, number)
        record["evidence_url"] = API_BASE + parse.quote(doi, safe="")
        if not online:
            record.update(status="not_checked_offline", reason="no_network_request_made")
            continue
        if doi not in cache:
            if stop_reason:
                record.update(status="network_error", reason=stop_reason)
                continue
            if cache:
                sleeper(REQUEST_INTERVAL_SECONDS)
            fetched = fetch_metadata(doi, transport)
            cache[doi] = fetched
            if fetched["stop_batch"]:
                stop_reason = "batch_stopped_after_" + fetched["reason"]
        fetched = cache[doi]
        for field in ("retrieved", "checked_at", "evidence_url"):
            record[field] = fetched[field]
        if "status" in fetched:
            record.update(status=fetched["status"], reason=fetched["reason"])
            continue
        record["mismatches"] = compare_metadata(record, fetched["retrieved"])
        record.update(status="metadata_mismatch" if record["mismatches"] else "verified_metadata",
                      reason="supplied_doi_title_year_compared_with_crossref_only")
    return {
        "schema_version": 1, "mode": "online" if online else "offline",
        "generated_at": utc_now(),
        "scope": "DOI/title/year metadata only; no full-text, claim, correction, or retraction verification",
        "summary": {status: sum(record["status"] == status for record in records)
                    for status in STATUSES},
        "records": records,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 CSV with doi,title,year headers")
    parser.add_argument("--output", required=True, type=Path, help="JSON report path")
    parser.add_argument("--online", action="store_true", help="send DOI identifiers to Crossref")
    args = parser.parse_args(argv)
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("input and output paths must differ")
        if args.output.exists():
            raise ValueError("output exists; choose a new report path")
        with args.input.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            if (not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames))
                    or not {"doi", "title", "year"}.issubset(reader.fieldnames)):
                raise ValueError("CSV needs unique, case-sensitive doi,title,year headers")
            rows = []
            for row in reader:
                rows.append(row)
                if len(rows) > MAX_ROWS:
                    raise ValueError(f"at most {MAX_ROWS} rows per invocation")
        if not rows:
            raise ValueError("CSV must include at least one data row")
        report = verify_rows(rows, online=args.online)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"Input/output error: {exc}", file=sys.stderr)
        return 2
    return 0 if all(row["status"] == "verified_metadata" for row in report["records"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
