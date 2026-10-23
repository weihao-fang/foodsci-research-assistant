"""SYNTHETIC: descriptive paired analysis; Python standard library only.

Run: python analyze.py INPUT_CSV OUTPUT_DIRECTORY
Two technical wells are averaged before four production-day pairs are compared.
"""
import csv
import hashlib
import json
import platform
from pathlib import Path
from statistics import mean, stdev
import sys


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def describe(values):
    return {"n": len(values), "mean": mean(values), "sd": stdev(values),
            "min": min(values), "max": max(values)}


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


raw_path, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
with raw_path.open(encoding="utf-8-sig", newline="") as f:
    raw = list(csv.DictReader(f))
assert len(raw) == 8
units = []
for line, row in enumerate(raw, start=2):
    assert row["dataset_status"] == "SYNTHETIC"
    assert all(value != "" for value in row.values())
    mass = float(row["wet_mass_g"])
    volume = float(row["extract_volume_mL"])
    dilution = float(row["dilution_factor"])
    dry_fraction = float(row["dry_matter_fraction"])
    assert mass > 0 and volume > 0 and dilution > 0 and 0 < dry_fraction <= 1
    net = [float(row[f"A_FC_{i}"]) - float(row[f"A_background_{i}"])
           for i in (1, 2)]
    net_mean = mean(net)
    diluted_ug_mL = 100 * net_mean
    extract_ug_mL = diluted_ug_mL * dilution
    extracted_mg = extract_ug_mL * volume / 1000
    wet = extracted_mg / mass
    dry = wet / dry_fraction
    units.append({"dataset_status": "SYNTHETIC", "source_csv_line": line,
                  "sample_id": row["batch"] + "-" + row["treatment"],
                  "batch": row["batch"], "treatment": row["treatment"],
                  "technical_wells": 2, "net_A_1": net[0], "net_A_2": net[1],
                  "net_A_mean": net_mean, "diluted_ug_GAE_mL": diluted_ug_mL,
                  "extract_ug_GAE_mL": extract_ug_mL,
                  "extracted_mg_GAE": extracted_mg,
                  "dry_matter_fraction_g_g": dry_fraction,
                  "aliquot_dry_mass_g": mass * dry_fraction,
                  "wet_mg_GAE_g": wet, "dry_mg_GAE_g": dry})

by_id = {(u["batch"], u["treatment"]): u for u in units}
assert len(by_id) == 8
assert set(by_id) == {(b, t) for b in ("B1", "B2", "B3", "B4") for t in ("C", "H")}
pairs = []
for batch in ("B1", "B2", "B3", "B4"):
    c, h = by_id[(batch, "C")], by_id[(batch, "H")]
    pair = {"dataset_status": "SYNTHETIC", "batch": batch}
    for basis in ("wet", "dry"):
        key = basis + "_mg_GAE_g"
        pair.update({basis + "_C_mg_GAE_g": c[key],
                     basis + "_H_mg_GAE_g": h[key],
                     basis + "_H_minus_C_mg_GAE_g": h[key] - c[key],
                     basis + "_change_percent_of_C": 100 * (h[key] / c[key] - 1)})
    pairs.append(pair)

summary = {"dataset_status": "SYNTHETIC", "analysis": "paired descriptive",
           "independent_units": "4 production-day batches; C/H split from each batch",
           "technical_replication": "2 wells per single extract; averaged before comparison",
           "variation": "sample SD (n-1), among four batch values or four paired changes",
           "no_inference": "No hypothesis test or population confidence interval computed",
           "results": {},
           "quality": {"raw_rows": 8, "unique_batch_treatment_units": 8,
                       "complete_pairs": 4, "technical_wells_total": 16,
                       "missing_cells": 0, "excluded_rows": [],
                       "all_background_corrected_readings_positive": all(u["net_A_1"] > 0 and u["net_A_2"] > 0 for u in units)},
           "environment": {"python": platform.python_version(), "packages": "standard library only",
                           "command_arguments": sys.argv, "random_seed": None,
                           "raw_sha256": sha256(raw_path), "code_sha256": sha256(Path(__file__))}}
for basis in ("wet", "dry"):
    key = basis + "_mg_GAE_g"
    c = [u[key] for u in units if u["treatment"] == "C"]
    h = [u[key] for u in units if u["treatment"] == "H"]
    summary["results"][basis] = {
        "units": "mg GAE/g wet slurry" if basis == "wet" else "mg GAE/g dry matter",
        "C": describe(c), "H": describe(h),
        "paired_H_minus_C": describe([p[basis + "_H_minus_C_mg_GAE_g"] for p in pairs]),
        "paired_change_percent_of_C": describe([p[basis + "_change_percent_of_C"] for p in pairs]),
        "percent_change_of_group_means": 100 * (mean(h) / mean(c) - 1),
        "positive_pairs": sum(p[basis + "_H_minus_C_mg_GAE_g"] > 0 for p in pairs),
        "negative_pairs": sum(p[basis + "_H_minus_C_mg_GAE_g"] < 0 for p in pairs)}
write_csv(out / "unit-values.csv", units)
write_csv(out / "paired-changes.csv", pairs)
(out / "analysis.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"dataset_status": "SYNTHETIC", "quality": summary["quality"],
                  "results": summary["results"]}, ensure_ascii=False, indent=2))
