"""Traceable descriptive summaries; Python 3.10+, standard library only."""
import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def read_csv(path, required):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError("Duplicate CSV column names")
        missing = set(required) - set(fields)
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        rows = []
        for line, row in enumerate(reader, 2):
            if None in row or any(not (row.get(k) or "").strip() for k in required):
                raise ValueError(f"CSV record {line}: missing fields or extra values")
            row = {k: (v or "").strip() for k, v in row.items()}
            row["source_record"] = line
            rows.append(row)
        if not rows:
            raise ValueError("No observations")
        return rows


def number(row, field):
    try:
        value = float(row[field])
    except (ValueError, TypeError):
        raise ValueError(f"Record {row['source_record']}: {field} is not numeric") from None
    if not math.isfinite(value):
        raise ValueError(f"Record {row['source_record']}: {field} must be finite")
    return value


def describe(values):
    return {"n_biological": len(values), "mean": statistics.mean(values),
            "sd": statistics.stdev(values) if len(values) > 1 else None}


def check_unique(rows, keys):
    seen = set()
    for row in rows:
        key = tuple(row[k] for k in keys)
        if key in seen:
            raise ValueError(f"Duplicate observation {key}")
        seen.add(key)


def check_units(rows, field):
    units = defaultdict(set)
    for row in rows:
        units[row[field]].add(row["unit"])
    if any(len(value) != 1 for value in units.values()):
        raise ValueError(f"Mixed units for the same {field}; convert explicitly first")


def raw_summary(rows, reference_group):
    """Normalize per matched plate, then average plates within independent experiments."""
    required = ("experiment_id", "plate_id", "well", "group", "endpoint", "value", "blank", "unit")
    if any(any(k not in row for k in required) for row in rows):
        raise ValueError("RAW columns incomplete")
    check_unique(rows, ("experiment_id", "plate_id", "well", "endpoint"))
    check_units(rows, "endpoint")
    wells = defaultdict(list)
    for row in rows:
        corrected = number(row, "value") - number(row, "blank")
        if not math.isfinite(corrected):
            raise ValueError("Nonfinite blank-corrected signal")
        key = tuple(row[k] for k in ("experiment_id", "plate_id", "endpoint", "unit", "group"))
        wells[key].append({"well": row["well"], "source_record": row["source_record"],
                           "corrected": corrected})
    means = {key: statistics.mean(w["corrected"] for w in value) for key, value in wells.items()}
    warnings = []
    plates = []
    biological = defaultdict(list)
    for key, value in wells.items():
        experiment, plate, endpoint, unit, group = key
        ref_key = (experiment, plate, endpoint, unit, reference_group)
        if ref_key not in means or means[ref_key] <= 0:
            raise ValueError(f"Missing or nonpositive matched reference for {key}")
        ratio = means[key] / means[ref_key] * 100
        if not math.isfinite(ratio):
            raise ValueError("Nonfinite reference normalization")
        if any(w["corrected"] < 0 for w in value):
            warnings.append(f"Negative corrected signal: {key}; values retained, inspect blanks")
        item = dict(zip(("experiment_id", "plate_id", "endpoint", "unit", "group"), key))
        item.update(mean_corrected=means[key], reference_mean_corrected=means[ref_key],
                    normalized_percent=ratio, n_technical=len(value), observations=value)
        plates.append(item)
        biological[(experiment, endpoint, unit, group)].append(item)
    replicate_rows = []
    groups = defaultdict(list)
    for key, items in biological.items():
        item = dict(zip(("experiment_id", "endpoint", "unit", "group"), key))
        item.update(mean_corrected=statistics.mean(x["mean_corrected"] for x in items),
                    normalized_percent=statistics.mean(x["normalized_percent"] for x in items),
                    n_plates=len(items))
        replicate_rows.append(item)
        groups[key[1:]].append(item)
    summaries = []
    for (endpoint, unit, group), items in groups.items():
        summaries.append({"endpoint": endpoint, "unit": unit, "group": group,
                          "corrected": describe([x["mean_corrected"] for x in items]),
                          "normalized_percent": describe([x["normalized_percent"] for x in items]),
                          "experiment_ids": [x["experiment_id"] for x in items]})
        if len(items) == 1:
            warnings.append(f"Only one independent experiment: {endpoint}/{group}; SD undefined")
    return {"mode": "raw", "reference_group": reference_group,
            "plate_summaries": plates, "biological_replicates": replicate_rows,
            "group_summaries": summaries, "warnings": warnings}


def digestion_summary(rows):
    check_unique(rows, ("experiment_id", "sample_id", "stage", "replicate_id", "readout"))
    check_units(rows, "readout")
    technical = defaultdict(list)
    warnings = []
    for row in rows:
        factor = number(row, "dilution_factor")
        if factor <= 0:
            raise ValueError("dilution_factor must be positive")
        adjusted = (number(row, "value") - number(row, "blank")) * factor
        if not math.isfinite(adjusted):
            raise ValueError("Nonfinite corrected/dilution-adjusted value")
        if adjusted < 0:
            warnings.append(f"Negative corrected value at record {row['source_record']}; retained")
        key = tuple(row[k] for k in ("experiment_id", "sample_id", "stage", "readout", "unit"))
        technical[key].append({"replicate_id": row["replicate_id"],
                               "source_record": row["source_record"], "adjusted": adjusted})
    biological = []
    groups = defaultdict(list)
    for key, observations in technical.items():
        item = dict(zip(("experiment_id", "sample_id", "stage", "readout", "unit"), key))
        item.update(mean_adjusted=statistics.mean(x["adjusted"] for x in observations),
                    n_technical=len(observations), observations=observations)
        biological.append(item)
        groups[key[1:]].append(item)
    summaries = []
    for key, items in groups.items():
        item = dict(zip(("sample_id", "stage", "readout", "unit"), key))
        item.update(describe([x["mean_adjusted"] for x in items]))
        item["experiment_ids"] = [x["experiment_id"] for x in items]
        summaries.append(item)
        if len(items) == 1:
            warnings.append(f"Only one independent digestion: {key}; SD undefined")
    return {"mode": "digestion", "biological_replicates": biological,
            "group_summaries": summaries, "warnings": warnings}


RAW_FIELDS = "experiment_id plate_id well group endpoint value blank unit".split()
DIGESTION_FIELDS = "experiment_id sample_id stage replicate_id readout value blank unit dilution_factor".split()


def analyze(path, mode, reference_group=None):
    if mode not in ("raw", "digestion"):
        raise ValueError("Unknown analysis mode")
    if mode == "raw" and not reference_group:
        raise ValueError("RAW analysis requires an explicit reference group")
    rows = read_csv(path, RAW_FIELDS if mode == "raw" else DIGESTION_FIELDS)
    result = raw_summary(rows, reference_group) if mode == "raw" else digestion_summary(rows)
    result.update(input_file=str(Path(path).resolve()),
                  input_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                  generated_at=datetime.now(timezone.utc).isoformat(),
                  n_input_records=len(rows), inference="descriptive_only_no_p_values",
                  assumption="experiment_id denotes user-confirmed independent biological units")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("raw", "digestion"))
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--reference-group")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Output must not overwrite input")
    try:
        result = analyze(args.input, args.mode, args.reference_group)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"Analysis failed: {error}\n")


if __name__ == "__main__":
    main()
