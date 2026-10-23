import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_workflow", ROOT / "scripts/run_workflow.py")
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class WorkflowTests(unittest.TestCase):
    def test_complete_demo_distinguishes_doi_review_from_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "results"
            report = workflow.run_workflow(ROOT / "assets/examples/workflow.json", output)
            self.assertEqual(report["status"], "completed")
            self.assertTrue(report["needs_review"])
            self.assertEqual(report["tasks"][2]["status"], "needs_review")
            self.assertEqual(report["not_run"], [])
            raw = json.loads((output / "raw-summary.json").read_text(encoding="utf-8"))
            sample = next(x for x in raw["group_summaries"] if x["group"] == "treatment")
            self.assertAlmostEqual(sample["normalized_percent"]["mean"], 85)
            self.assertEqual(sample["corrected"]["n_biological"], 2)
            digestion = json.loads((output / "digestion-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(digestion["group_summaries"][0]["mean"], 15)

    def test_failed_analysis_stops_following_task(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary)
            bad = temporary / "bad.csv"
            bad.write_text("invalid\n", encoding="utf-8")
            config = temporary / "workflow.json"
            config.write_text(json.dumps({"tasks": [
                {"id": "bad", "mode": "digestion", "input": "bad.csv"},
                {"id": "later", "mode": "digestion", "input": "bad.csv"}]}), encoding="utf-8")
            result = workflow.run_workflow(config, temporary / "results")
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["not_run"], ["later"])
            self.assertFalse((temporary / "results/later.json").exists())

    def test_invalid_ids_rejected_before_creating_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary)
            config = temporary / "workflow.json"
            config.write_text(json.dumps({"tasks": [{"id": "../escape", "mode": "raw", "input": "x"}]}))
            with self.assertRaisesRegex(ValueError, "Task ids"):
                workflow.run_workflow(config, temporary / "results")
            self.assertFalse((temporary / "results").exists())

    def test_existing_output_dir_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(FileExistsError):
                workflow.run_workflow(ROOT / "assets/examples/workflow.json", Path(temporary))

    def test_report_filename_is_reserved_before_creating_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary)
            config = temporary / "workflow.json"
            config.write_text(json.dumps({"tasks": [{"id": "run-report", "mode": "digestion",
                "input": str(ROOT / "assets/examples/SYNTHETIC_digestion.csv")}]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "reserved"):
                workflow.run_workflow(config, temporary / "results")
            self.assertFalse((temporary / "results").exists())

    def test_chinese_diagnostic_survives_non_utf8_parent_console(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary)
            (temporary / "raw.csv").write_text(
                "experiment_id,plate_id,well,group,endpoint,value,blank,unit\n"
                "E1,P1,A1,样品组,signal,1,0,AU\n", encoding="utf-8")
            config = temporary / "workflow.json"
            config.write_text(json.dumps({"tasks": [{"id": "raw", "mode": "raw",
                "input": "raw.csv", "reference_group": "对照组"}]}), encoding="utf-8")
            env = dict(os.environ, PYTHONIOENCODING="gbk")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/run_workflow.py"),
                "--config", str(config), "--output-dir", str(temporary / "results")],
                env=env, capture_output=True)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn(b"Traceback", run.stderr)
            report = json.loads(run.stdout)
            self.assertIn("样品组", report["tasks"][0]["stderr"])
            self.assertNotIn("\ufffd", report["tasks"][0]["stderr"])


if __name__ == "__main__":
    unittest.main()
