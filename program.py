import os
import tarfile
import bz2
from compression import zstd
import argparse
from pathlib import Path
import time
import sys


def main():
    parser = argparse.ArgumentParser(description='zstd bz2 архиватор')

    parser.add_argument('-b', '--benchmark', action='store_true',
                        help='Включить/Отключить замер времени')

    subparsers = parser.add_subparsers(dest='commands', help='Доступные команды')

    create_parser = subparsers.add_parser('create', help='Создать архив')
    create_parser.add_argument('source', help='Путь архивации')
    create_parser.add_argument('output', help='Итоговый архив')

    extract_parser = subparsers.add_parser('extract', help='Распаковать архив')
    extract_parser.add_argument('archive', help='Файл архива для распаковки')
    extract_parser.add_argument('output', help='Путь распаковки')

    args = parser.parse_args()

    if args.commands == 'create':
        create_archive(args.source, args.output, benchmark_mode=args.benchmark)
    elif args.commands == 'extract':
        extract_archive(args.archive, args.output, benchmark_mode=args.benchmark)
    else:
        parser.print_help()

def create_archive(source, output, benchmark_mode=False):
    source = Path(source)
    output = Path(output)
    if not source.exists():
        print("Выбранная директория не существует")
        return False

    fileType=output.suffix
    if benchmark_mode: startTime = time.time()

    if fileType == '.bz2':
        compress_bz2(source, output)
    elif fileType == '.zstd':
        compress_zstd(source, output)
    else:
        print("Выбрано неверное разрешение файла")

    if benchmark_mode:
        endTime = time.time()
        print(f"Время архивации: {endTime - startTime} секунд")


def extract_archive(archive, output, benchmark_mode=False):
    source = Path(archive)
    output = Path(output)
    if not source.exists():
        print(f"Выбранная директория {source} не существует")
        return False

    if not output.exists():
        print(f"Выбранная директория {output} не существует")
        return False

    fileType = source.suffix
    if benchmark_mode:
        startTime = time.time()

    if fileType == '.bz2':
        decompress_bz2(source, output)
    elif fileType == '.zstd':
        decompress_zstd(source, output)
    else:
        print("Выбрано неверное разрешение файла")

    if benchmark_mode:
        endTime = time.time()
        print(f"Время извлечения: {endTime - startTime} секунд")

def compress_bz2(source, output):

    if source.is_dir():
        tempTar=str(output)+".temp.tar"
        with tarfile.open(tempTar, "w") as tar:
            tar.add(source, arcname=source.name)
    else:
        tempTar=source

    with open (tempTar,"rb") as f1, bz2.open(output,"wb") as f2:

        total_size = os.path.getsize(tempTar)
        copy_with_progress(f1, f2, total_size)

    if source.is_dir():
        if os.path.exists(tempTar):
            os.remove(tempTar)

    print(f"Архив сохранен в {output}")


def compress_zstd(source, output):

    if source.is_dir():
        tempTar = str(output) + ".temp.tar"
        with tarfile.open(tempTar, "w") as tar:
            tar.add(source, arcname=source.name)
    else:
        tempTar = source

    with open(tempTar, "rb") as f1, zstd.open(output, "wb") as f2:
        total_size = os.path.getsize(tempTar)
        copy_with_progress(f1, f2, total_size)

    if source.is_dir() and os.path.exists(tempTar):
        os.remove(tempTar)

    print(f"Архив сохранен в {output}")


def decompress_bz2(source, output):
    tempFileName= output/(source.stem + ".temp.untar")

    with bz2.BZ2File(source,"rb") as f1, bz2.BZ2File(tempFileName,"wb") as f2:
        total_size = os.path.getsize(source)
        copy_with_progress(f1, f2, total_size)
    try:
        with tarfile.open(tempFileName,"r") as tar:
            tar.extractall(path=output)
    except tarfile.ReadError:
        fileName = output/source.stem
        os.rename(tempFileName, fileName)

    if tempFileName.exists():
        tempFileName.unlink()

def decompress_zstd(source, output):
    tempFileName= output/(source.stem + ".temp.untar")

    with zstd.open(source,"rb") as f1, bz2.open(tempFileName,"wb") as f2:
        total_size = os.path.getsize(source)
        copy_with_progress(f1, f2, total_size)
    try:
        with tarfile.open(tempFileName,"r") as tar:
            tar.extractall(path=output)
    except tarfile.ReadError:
        fileName = output/source.stem
        os.rename(tempFileName, fileName)

    if tempFileName.exists():
        tempFileName.unlink()

def progress(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    fmt = '[%s] %s%s %s' % (bar, percents, '%', status)
    print('\r' + fmt, end='')  # clears the line
    # sys.stdout.write(fmt)
    # sys.stdout.flush()

def copy_with_progress(str,dst,total_size,chunk_size=1024*1024):
    copied=0
    while True:
        chunk=str.read(chunk_size)
        if not chunk: break
        dst.write(chunk)
        copied+=len(chunk)

        if copied>total_size:
            copied=total_size

        progress(copied, total_size)
    print()

if __name__ == '__main__':
    main()

