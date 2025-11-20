import os
import sys
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)

INPUT_DIR = "/workspace/input"
OUTPUT_DIR = "/workspace/output"

def main():
    # Создаём output (если нет) и ставим права
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        os.chmod(OUTPUT_DIR, 0o777)
    except:
        logging.warning("Ай-ай-ай! Не удалось установить права 777 для output")

    # Пути ко входным файлам
    meta_path = os.path.join(INPUT_DIR, "samples_meta.csv")
    ms_path = os.path.join(INPUT_DIR, "ms_signal.csv")
    qc_path = os.path.join(INPUT_DIR, "qc_metrics.csv")

    logging.info("Чтение исходных данных")
    meta = pd.read_csv(meta_path)
    ms = pd.read_csv(ms_path)
    qc = pd.read_csv(qc_path)

    logging.info(f"meta: {meta.shape}")
    logging.info(f"ms:   {ms.shape}")
    logging.info(f"qc:   {qc.shape}")

    # INNER JOIN
    logging.info("INNER JOIN")
    inner = meta.merge(ms, on="sample_id", how="inner").merge(qc, on="sample_id", how="inner")
    inner.to_csv(os.path.join(OUTPUT_DIR, "inner_join_result.csv"), index=False)
    logging.info(f"INNER есть: {len(inner)} строк")

    # LEFT JOIN
    logging.info("LEFT JOIN")
    left = meta.merge(ms, on="sample_id", how="left").merge(qc, on="sample_id", how="left")
    left.to_csv(os.path.join(OUTPUT_DIR, "left_join_result.csv"), index=False)
    logging.info(f"LEFT есть: {len(left)} строк")

    # RIGHT JOIN
    logging.info("RIGHT JOIN")
    right = meta.merge(ms, on="sample_id", how="right").merge(qc, on="sample_id", how="left")
    right.to_csv(os.path.join(OUTPUT_DIR, "right_join_result.csv"), index=False)
    logging.info(f"RIGHT есть: {len(right)} строк")

    # OUTER JOIN
    logging.info("OUTER JOIN")
    outer = meta.merge(ms, on="sample_id", how="outer").merge(qc, on="sample_id", how="outer")
    outer.to_csv(os.path.join(OUTPUT_DIR, "outer_join_result.csv"), index=False)
    logging.info(f"OUTER есть: {len(outer)} строк")

    logging.info("Парам-парам-пам! (вжух) Все! (у меня тут Ералаш на фоне)")


if __name__ == "__main__":
    main()
