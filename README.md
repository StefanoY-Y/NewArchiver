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
```
```bash
python program.py -b create test compressed.zstd
```

### Распаковка архива
```bash
python program.py -b extract compressed.bz2 decompressed   
```
```bash
python program.py -b extract compressed.zstd decompressed 
```
## Скриншоты
### Архивация zst
![Image alt](https://github.com/StefanoY-Y/NewArchiver/blob/master/Screenshots/Screenshot_1.png)
### Архивация bz2
![Image alt](https://github.com/StefanoY-Y/NewArchiver/blob/master/Screenshots/Screenshot_2.png)
### Распаковка zst
![Image alt](https://github.com/StefanoY-Y/NewArchiver/blob/master/Screenshots/Screenshot_3.png)
### Распаковка bz2
![Image alt](https://github.com/StefanoY-Y/NewArchiver/blob/master/Screenshots/Screenshot_4.png)
