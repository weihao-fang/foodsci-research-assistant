"""Synthetic fixtures only: no DOI in this module is presented as a real source."""

import contextlib
import importlib.util
import io
from http.client import IncompleteRead
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "verify_doi.py"
SPEC = importlib.util.spec_from_file_location("verify_doi", MODULE_PATH)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def synthetic_row(**overrides):
    return {"doi": "10.9999/synthetic-unit-test", "title": "Synthetic Food Study", "year": "2024", **overrides}


def synthetic_response(**overrides):
    metadata = {"DOI": "10.9999/synthetic-unit-test", "title": ["Synthetic Food Study"],
                "published": {"date-parts": [[2024, 1, 1]]}, **overrides}
    return io.StringIO(json.dumps({"message": metadata}))


class VerifyDoiTests(unittest.TestCase):
    def test_offline_cannot_verify_or_send_request(self):
        transport = Mock(side_effect=AssertionError("offline network access"))
        record = verifier.verify_rows([synthetic_row()], transport=transport)["records"][0]
        self.assertEqual(record["status"], "not_checked_offline")
        self.assertIsNone(record["checked_at"])
        self.assertIsNone(record["retrieved"])
        transport.assert_not_called()

    def test_metadata_match_normalizes_doi_url_case_and_title(self):
        transport = Mock(return_value=synthetic_response(title=["Synthetic Food: Study!"]))
        row = synthetic_row(doi="HTTPS://DOI.ORG/10.9999%2FSYNTHETIC-UNIT-TEST",
                            title="Ｓｙｎｔｈｅｔｉｃ Food Study")
        record = verifier.verify_rows([row], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "verified_metadata")
        self.assertTrue(record["checked_at"])
        self.assertEqual(transport.call_args.kwargs["timeout"], 15)
        self.assertEqual(transport.call_args.args[0].full_url,
                         "https://api.crossref.org/works/10.9999%2Fsynthetic-unit-test")

    def test_doi_mismatch_cannot_verify_title_and_year_match(self):
        transport = Mock(return_value=synthetic_response(DOI="10.9999/other-synthetic-test"))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "metadata_mismatch")
        self.assertEqual(record["mismatches"], ["doi"])
        self.assertEqual(record["retrieved"]["doi"], "10.9999/other-synthetic-test")

    def test_scientific_comparison_text_cannot_disappear_as_html(self):
        for expected, actual in [("Effects at pH < 5 and dose > 10", "Effects at pH 10"),
                                 ("x<y and z>w", "xw"), ("T<Tc and P>Pcrit", "TPcrit")]:
            with self.subTest(expected=expected):
                transport = Mock(return_value=synthetic_response(title=[actual]))
                record = verifier.verify_rows([synthetic_row(title=expected)],
                                              online=True, transport=transport)["records"][0]
                self.assertEqual(record["status"], "metadata_mismatch")
                self.assertEqual(record["mismatches"], ["title"])

    def test_opposite_comparison_and_charge_signs_do_not_match(self):
        for expected, actual in [("Dose <5", "Dose >5"), ("CD4+ cells", "CD4- cells")]:
            with self.subTest(expected=expected):
                transport = Mock(return_value=synthetic_response(title=[actual]))
                record = verifier.verify_rows([synthetic_row(title=expected)], online=True,
                                              transport=transport)["records"][0]
                self.assertEqual(record["status"], "metadata_mismatch")

    def test_html_markup_and_entities_match_the_same_scientific_text(self):
        for actual in ("<i>Effects</i> at pH &lt; 5", "Effects at pH < 5",
                       "<jats:italic>Effects</jats:italic> at pH &lt; 5"):
            with self.subTest(actual=actual):
                transport = Mock(return_value=synthetic_response(title=[actual]))
                record = verifier.verify_rows([synthetic_row(title="Effects at pH < 5")],
                                              online=True, transport=transport)["records"][0]
                self.assertEqual(record["status"], "verified_metadata")

    def test_title_and_year_mismatch_show_both_expected_and_retrieved(self):
        transport = Mock(return_value=synthetic_response(title=["Different synthetic title"],
                         published={"date-parts": [[2023]]}))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "metadata_mismatch")
        self.assertEqual(record["mismatches"], ["title", "year"])
        self.assertEqual(record["expected"]["year"], "2024")
        self.assertEqual(record["retrieved"]["publication_years"], [2023])

    def test_online_and_print_publication_years_are_explicit(self):
        transport = Mock(return_value=synthetic_response(**{
            "published-online": {"date-parts": [[2023]]},
            "published-print": {"date-parts": [[2025]]}}))
        record = verifier.verify_rows([synthetic_row(year="2025")], online=True,
                                      transport=transport)["records"][0]
        self.assertEqual(record["status"], "verified_metadata")
        self.assertEqual(record["retrieved"]["publication_years"], [2023, 2024, 2025])

    def test_network_failure_is_never_verified(self):
        transport = Mock(side_effect=URLError("synthetic connection failure"))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "network_error")
        self.assertIsNone(record["retrieved"])
        self.assertTrue(record["checked_at"])
        self.assertEqual(transport.call_count, 1)

    def test_timeout_is_reported_without_retry(self):
        transport = Mock(side_effect=TimeoutError("synthetic timeout"))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "network_error")
        self.assertEqual(transport.call_count, 1)

    def test_truncated_response_is_reported_and_later_record_runs(self):
        broken = io.StringIO("")
        broken.read = Mock(side_effect=IncompleteRead(b"{", 10))
        transport = Mock(side_effect=[broken, synthetic_response(DOI="10.9999/second-synthetic")])
        report = verifier.verify_rows([synthetic_row(), synthetic_row(doi="10.9999/second-synthetic")],
                                      online=True, transport=transport, sleeper=Mock())
        self.assertEqual(report["records"][0]["status"], "network_error")
        self.assertIsNone(report["records"][0]["retrieved"])
        self.assertEqual(report["records"][1]["status"], "verified_metadata")
        self.assertEqual(transport.call_count, 2)

    def test_404_means_crossref_not_found(self):
        transport = Mock(side_effect=HTTPError("https://api.crossref.org/", 404, "synthetic", {}, None))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "not_found")

    def test_rate_limit_stops_new_requests(self):
        transport = Mock(side_effect=HTTPError("https://api.crossref.org/", 429, "synthetic", {}, None))
        report = verifier.verify_rows([synthetic_row(), synthetic_row(doi="10.9999/second-synthetic")],
                                      online=True, transport=transport)
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(report["records"][1]["status"], "network_error")
        self.assertIsNone(report["records"][1]["checked_at"])

    def test_duplicate_doi_uses_one_request_but_compares_each_row(self):
        transport = Mock(return_value=synthetic_response())
        sleeper = Mock()
        rows = [synthetic_row(), synthetic_row(doi="doi:10.9999/SYNTHETIC-UNIT-TEST",
                                               title="Wrong synthetic title")]
        records = verifier.verify_rows(rows, online=True, transport=transport,
                                       sleeper=sleeper)["records"]
        self.assertEqual(transport.call_count, 1)
        sleeper.assert_not_called()
        self.assertEqual(records[0]["status"], "verified_metadata")
        self.assertEqual(records[1]["status"], "metadata_mismatch")
        self.assertEqual(records[1]["duplicate_of_row"], 2)

    def test_distinct_dois_are_rate_limited(self):
        transport = Mock(side_effect=[synthetic_response(), synthetic_response(DOI="10.9999/second-synthetic")])
        sleeper = Mock()
        verifier.verify_rows([synthetic_row(), synthetic_row(doi="10.9999/second-synthetic")],
                             online=True, transport=transport, sleeper=sleeper)
        sleeper.assert_called_once_with(1)

    def test_missing_metadata_is_not_verified(self):
        transport = Mock(return_value=synthetic_response(title=[], published={}))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "metadata_mismatch")
        self.assertEqual(record["mismatches"], ["title", "year"])

    def test_malformed_server_response_is_not_verification(self):
        transport = Mock(return_value=io.StringIO("not JSON"))
        record = verifier.verify_rows([synthetic_row()], online=True, transport=transport)["records"][0]
        self.assertEqual(record["status"], "network_error")

    def test_invalid_rows_do_not_send_requests(self):
        transport = Mock()
        for row in [synthetic_row(doi="not-a-doi"), synthetic_row(year="24"),
                    synthetic_row(title=""), synthetic_row(title="< > + -")]:
            with self.subTest(row=row):
                record = verifier.verify_rows([row], online=True, transport=transport)["records"][0]
                self.assertEqual(record["status"], "invalid_input")
                self.assertIsNone(record["checked_at"])
        transport.assert_not_called()

    def test_cli_offline_exit_code_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            source, report = Path(directory) / "input.csv", Path(directory) / "report.json"
            source.write_text("doi,title,year\n10.9999/synthetic-unit-test,Synthetic Food Study,2024\n", encoding="utf-8")
            with patch.object(verifier.request, "urlopen", side_effect=AssertionError("offline network access")):
                code = verifier.main(["--input", str(source), "--output", str(report)])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["summary"]["not_checked_offline"], 1)

    def test_invalid_headers_fail_before_network_and_report_write(self):
        with tempfile.TemporaryDirectory() as directory:
            source, report = Path(directory) / "input.csv", Path(directory) / "report.json"
            source.write_text("doi,title\n10.9999/synthetic-unit-test,Synthetic Food Study\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), patch.object(verifier.request, "urlopen") as transport:
                code = verifier.main(["--input", str(source), "--output", str(report), "--online"])
            self.assertEqual(code, 2)
            self.assertFalse(report.exists())
            transport.assert_not_called()

    def test_existing_report_is_preserved_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            source, report = Path(directory) / "input.csv", Path(directory) / "report.json"
            source.write_text("doi,title,year\n10.9999/synthetic-unit-test,Synthetic Food Study,2024\n", encoding="utf-8")
            report.write_text("existing", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), patch.object(verifier.request, "urlopen") as transport:
                code = verifier.main(["--input", str(source), "--output", str(report), "--online"])
            self.assertEqual(code, 2)
            self.assertEqual(report.read_text(encoding="utf-8"), "existing")
            transport.assert_not_called()

    def test_unclosed_csv_quote_fails_before_network_and_report_write(self):
        with tempfile.TemporaryDirectory() as directory:
            source, report = Path(directory) / "input.csv", Path(directory) / "report.json"
            source.write_text("doi,title,year,note\n"
                "10.9999/synthetic-unit-test,Synthetic Food Study,2024,\"unfinished\n"
                "10.9999/second-synthetic,Synthetic Food Study,2024,ok\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), patch.object(verifier.request, "urlopen") as transport:
                code = verifier.main(["--input", str(source), "--output", str(report), "--online"])
            self.assertEqual(code, 2)
            self.assertFalse(report.exists())
            transport.assert_not_called()


if __name__ == "__main__":
    unittest.main()
