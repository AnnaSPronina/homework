import argparse
import sys
import pandas as pd


def guess_key_column(left_cols, right_cols):
    CANDIDATE_KEYS = ["sample_id", "SampleID", "sample", "Sample"]

    for key in CANDIDATE_KEYS:
        if key in left_cols and key in right_cols:
            return key
    return None


def main():
    parser = argparse.ArgumentParser(description="Выполнить три антиджоина.")
    parser.add_argument("--mass-spec", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--mass-without-metadata", required=True)
    parser.add_argument("--metadata-without-mass", required=True)
    parser.add_argument("--mismatched-samples", required=True)

    args = parser.parse_args()

    mass = pd.read_csv(args.mass_spec)
    meta = pd.read_csv(args.metadata)

    key = guess_key_column(mass.columns, meta.columns)
    if key is None:
        sys.stderr.write(
            f"Не найден ключевой столбец!\n"
            f"mass columns: {list(mass.columns)}\n"
            f"meta columns: {list(meta.columns)}\n"
        )
        sys.exit(1)

    mass_flag = mass.merge(meta[[key]].drop_duplicates(), on=key, how="left", indicator=True)
    mass_without_meta = mass_flag[mass_flag["_merge"] == "left_only"].drop(columns=["_merge"])

    meta_flag = meta.merge(mass[[key]].drop_duplicates(), on=key, how="left", indicator=True)
    meta_without_mass = meta_flag[meta_flag["_merge"] == "left_only"].drop(columns=["_merge"])

    mismatch_ids = pd.concat(
        [mass_without_meta[[key]], meta_without_mass[[key]]],
        ignore_index=True
    ).drop_duplicates()
    mismatch_ids = mismatch_ids.rename(columns={key: "sample_id_mismatched"})

    mass_without_meta.to_csv(args.mass_without_metadata, index=False)
    meta_without_mass.to_csv(args.metadata_without_mass, index=False)
    mismatch_ids.to_csv(args.mismatched_samples, index=False)


if __name__ == "__main__":
    main()
