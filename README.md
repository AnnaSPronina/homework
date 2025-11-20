# Project Overview

Этот проект демонстрирует объединение трёх связанных табличных наборов данных по `sample_id` с использованием четырёх типов JOIN-ов. Обработка упакована в Docker-контейнер, который читает входные CSV из каталога `input/` и сохраняет результаты в `output/`.

## Структура проекта

```text
.
├── input/                 # входные данные (примонтируются в контейнер)
├── output/                # сюда контейнер положит результаты join'ов
├── scripts/
│   ├── generate.py # генерация учебных CSV
│   └── join.py     # выполнение inner / left / right / outer join
├── Dockerfile
├── requirements.txt
└── README.md
```


## Что делает контейнер:

1. Загружает входные CSV из примонтированного каталога `input/`.
2. Выполняет:

   * INNER JOIN
   * LEFT JOIN
   * RIGHT JOIN
   * FULL OUTER JOIN
3. Логирует каждый шаг в консоль.
4. Записывает результаты в `output/`:

```
inner_join_result.csv
left_join_result.csv
right_join_result.csv
outer_join_result.csv
```

## Как запустить (для проверки результата):

```bash
docker run --rm \
  -v /path/to/input:/workspace/input \
  -v /path/to/output:/workspace/output \
  ms-joins-friend
```

При необходимости тестовые данные можно создать командой:

```bash
python scripts/make_input_data.py
```