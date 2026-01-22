# zstd-bz2 Archiver

Утилита для архивации и распаковки файлов с использованием форматов `.bz2` и `.zstd`.

## Ключи и команды

### Глобальные ключи
- `-b`, `--benchmark` — включить замер времени архивации/распаковки.

### Команды
- `create` — создать архив
  - Параметры:
    - `source` — путь к файлу или директории для архивации
    - `output` — имя итогового архива (с расширением `.bz2` или `.zstd`)
- `extract` — распаковать архив
  - Параметры:
    - `archive` — путь к архиву
    - `output` — директория для распаковки

## Примеры использования

### Создание архива
```bash
python program.py -b create test compressed.bz2   
python program.py -b create test compressed.zstd
```bash

### Распаковка архива
```bash
python program.py -b extract compressed.bz2 decompressed   
python program.py -b extract compressed.zstd decompressed 
```bash
