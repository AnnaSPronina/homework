# Mass-Spec Snakemake Pipeline

Этот проект выполняет:

1. Скачивание двух файлов данных в контейнере
2. Три антиджоина между mass_spec_results.csv и sample_metadata.csv
3. Полную оркестрацию пайплайна через Snakemake
4. Генерацию rulegraph.png и filegraph.png

Структура такая:
.
├── Snakefile
├── containers
│   ├── Dockerfile.download
│   └── Dockerfile.process
├── scripts
│   └── anti_joins.py
└── README.md