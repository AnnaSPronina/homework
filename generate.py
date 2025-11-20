"""
Генерация учебных данных для задания по джоинам.
Скрипт создаёт три CSV в папке `input`:
  - samples_meta.csv
  - ms_signal.csv
  - qc_metrics.csv
"""

import os
from datetime import datetime, timedelta
import random

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
INPUT_DIR = os.path.join(PROJECT_ROOT, "input")


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def build_sample_metadata(n: int = 20) -> pd.DataFrame:
    sample_ids = [f"SMPL_{i:03d}" for i in range(1, n + 1)]
    patients = [f"P{1000 + i}" for i in range(n)]
    groups = ["control", "treated"]

    start = datetime(2024, 2, 1)

    rows = []
    for sid, pid in zip(sample_ids, patients):
        rows.append(
            {
                "sample_id": sid,
                "patient_code": pid,
                "group_label": random.choice(groups),
                "collect_date": (start + timedelta(days=random.randint(0, 25))).strftime(
                    "%Y-%m-%d"
                ),
            }
        )
    return pd.DataFrame(rows)


def build_ms_results(sample_ids, n_features: int = 25) -> pd.DataFrame:
    rows = []
    for f_idx in range(1, n_features + 1):
        rows.append(
            {
                "sample_id": random.choice(sample_ids),
                "ms_feature": f"PEAK_{f_idx:04d}",
                "area": round(random.uniform(5e3, 8e5), 2),
            }
        )
    return pd.DataFrame(rows)


def build_quality(sample_ids, n_rows: int = 18) -> pd.DataFrame:
    flags = ["ok", "borderline", "bad"]
    rows = []
    for _ in range(n_rows):
        rows.append(
            {
                "sample_id": random.choice(sample_ids),
                "qc_status": random.choice(flags),
                "snr": round(random.uniform(5.0, 120.0), 2),
            }
        )
    return pd.DataFrame(rows)


def main():
    ensure_dir(INPUT_DIR)

    meta_df = build_sample_metadata()
    meta_df.to_csv(os.path.join(INPUT_DIR, "samples_meta.csv"), index=False)

    ms_df = build_ms_results(meta_df["sample_id"].tolist())
    ms_df.to_csv(os.path.join(INPUT_DIR, "ms_signal.csv"), index=False)

    qc_df = build_quality(meta_df["sample_id"].tolist())
    qc_df.to_csv(os.path.join(INPUT_DIR, "qc_metrics.csv"), index=False)

    print("Данные для примера сгенерированы в папку:", INPUT_DIR)
    for name in ["samples_meta.csv", "ms_signal.csv", "qc_metrics.csv"]:
        print(" -", name)


if __name__ == "__main__":
    main()
