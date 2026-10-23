import csv
import importlib.util
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analyze", ROOT / "scripts/analyze.py")
analyze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze)


def well(exp, name, value, group="sample", plate="P1", blank="0", unit="AU"):
    return dict(experiment_id=exp, plate_id=plate, well=name, group=group,
                endpoint="viability", value=str(value), blank=blank, unit=unit, source_record=2)


def digest(exp, rep, value, factor="2"):
    return dict(experiment_id=exp, sample_id="A", stage="intestinal", replicate_id=rep,
                readout="measured_concentration", value=str(value), blank="1", unit="mg/L",
                dilution_factor=factor, source_record=2)


class AnalyzeTests(unittest.TestCase):
    def test_technical_wells_do_not_inflate_n_or_weight_experiments(self):
        rows = [well("E1", "C1", 10, "control"), well("E2", "C1", 10, "control")]
        rows += [well("E1", f"S{i}", 5) for i in range(9)]
        rows += [well("E2", "S1", 9)]
        result = analyze.raw_summary(rows, "control")
        sample = next(x for x in result["group_summaries"] if x["group"] == "sample")
        self.assertEqual(sample["corrected"]["n_biological"], 2)
        self.assertEqual(sample["normalized_percent"]["mean"], 70)
        self.assertAlmostEqual(sample["normalized_percent"]["sd"], math.sqrt(800))

    def test_normalize_matched_plates_before_averaging(self):
        rows = [well("E1", "C", 10, "control"), well("E1", "S", 5),
                well("E1", "C", 100, "control", "P2"), well("E1", "S", 25, plate="P2")]
        result = analyze.raw_summary(rows, "control")
        sample = next(x for x in result["group_summaries"] if x["group"] == "sample")
        self.assertEqual(sample["normalized_percent"]["mean"], 37.5)
        self.assertEqual(sample["corrected"]["n_biological"], 1)
        self.assertIsNone(sample["corrected"]["sd"])

    def test_nonpositive_reference_rejected(self):
        for control in (0, -1):
            with self.assertRaisesRegex(ValueError, "reference"):
                analyze.raw_summary([well("E1", "C", control, "control"), well("E1", "S", 4)], "control")

    def test_reference_from_other_plate_not_reused(self):
        with self.assertRaisesRegex(ValueError, "reference"):
            analyze.raw_summary([well("E1", "C", 10, "control"), well("E1", "S", 4, plate="P2")], "control")

    def test_duplicate_well_rejected(self):
        row = well("E1", "C", 1, "control")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            analyze.raw_summary([row, row.copy()], "control")

    def test_mixed_endpoint_units_rejected(self):
        with self.assertRaisesRegex(ValueError, "Mixed units"):
            analyze.raw_summary([well("E1", "C", 1, "control"), well("E1", "S", 2, unit="mM")], "control")

    def test_nonfinite_signal_rejected(self):
        for value in ("NaN", "inf", "-inf"):
            with self.assertRaisesRegex(ValueError, "finite"):
                analyze.raw_summary([well("E1", "C", 1, "control"), well("E1", "S", value)], "control")

    def test_negative_corrected_signal_retained_with_warning(self):
        result = analyze.raw_summary([well("E1", "C", 1, "control"), well("E1", "S", 1, blank="2")], "control")
        self.assertTrue(any("Negative" in x for x in result["warnings"]))
        self.assertEqual(result["plate_summaries"][1]["mean_corrected"], -1)

    def test_digestion_correction_and_independent_n(self):
        result = analyze.digestion_summary([digest("E1", "T1", 3), digest("E1", "T2", 5), digest("E2", "T1", 6)])
        summary = result["group_summaries"][0]
        self.assertEqual(summary["n_biological"], 2)
        self.assertEqual(summary["mean"], 8)
        self.assertEqual(result["biological_replicates"][0]["n_technical"], 2)

    def test_digestion_nonpositive_factor_and_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            analyze.digestion_summary([digest("E1", "T1", 2, "0")])
        row = digest("E1", "T1", 2)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            analyze.digestion_summary([row, row.copy()])

    def test_cli_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "data.csv"
            with source.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=analyze.RAW_FIELDS)
                writer.writeheader()
                for row in [well("E1", "C", 1, "control"), well("E1", "S", 2)]:
                    writer.writerow({k: row[k] for k in analyze.RAW_FIELDS})
            target = directory / "result.json"
            target.write_text("existing", encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/analyze.py"), "raw", "--input", str(source),
                       "--output", str(target), "--reference-group", "control"]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(target.read_text(), "existing")
            self.assertNotIn("Traceback", run.stderr)

    def test_missing_values_and_empty_input_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.csv"
            source.write_text("value,blank\n1,\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing"):
                analyze.read_csv(source, ["value", "blank"])
            source.write_text("value,blank\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "No observations"):
                analyze.read_csv(source, ["value", "blank"])

    def test_unclosed_csv_quotes_rejected_without_writing_result(self):
        for column in ("unit", "note"):
            with self.subTest(column=column), tempfile.TemporaryDirectory() as directory:
                source, target = Path(directory) / "bad.csv", Path(directory) / "result.json"
                source.write_text(
                    "experiment_id,plate_id,well,group,endpoint,value,blank,unit,note\n"
                    "E1,P1,C,control,signal,10,0,AU,ok\n"
                    + ("E1,P1,S,sample,signal,5,0,\"AU,ok\n" if column == "unit"
                       else "E1,P1,S,sample,signal,5,0,AU,\"unfinished\n")
                    + "E2,P1,C,control,signal,10,0,AU,ok\n"
                    "E2,P1,S,sample,signal,9,0,AU,ok\n", encoding="utf-8")
                run = subprocess.run([sys.executable, str(ROOT / "scripts/analyze.py"),
                    "raw", "--input", str(source), "--output", str(target),
                    "--reference-group", "control"], capture_output=True, text=True)
                self.assertEqual(run.returncode, 2)
                self.assertFalse(target.exists())
                self.assertNotIn("Traceback", run.stderr)

    def test_valid_multiline_csv_note_preserves_observations(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "data.csv"
            source.write_text(
                "experiment_id,plate_id,well,group,endpoint,value,blank,unit,note\n"
                "E1,P1,C,control,signal,10,0,AU,ok\n"
                "E1,P1,S,sample,signal,5,0,AU,\"valid\nmultiline\"\n"
                "E2,P1,C,control,signal,10,0,AU,ok\n"
                "E2,P1,S,sample,signal,9,0,AU,ok\n", encoding="utf-8")
            rows = analyze.read_csv(source, analyze.RAW_FIELDS)
            self.assertEqual(len(rows), 4)
            self.assertEqual(rows[-1]["source_record"], 5)
            sample = next(x for x in analyze.raw_summary(rows, "control")["group_summaries"]
                          if x["group"] == "sample")
            self.assertEqual(sample["normalized_percent"]["mean"], 70)
            self.assertEqual(sample["corrected"]["n_biological"], 2)


if __name__ == "__main__":
    unittest.main()
