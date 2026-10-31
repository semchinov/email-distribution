# convert_xls.py

import csv
from pathlib import Path

import xlrd

from settings import settings


def cell_to_str(value) -> str:
    # xlrd отдаёт числа как float: 123.0 -> "123"
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value).strip()


def convert_xls_to_csv(
    xls_path: Path = settings.XLS_PATH,
    csv_path: Path = settings.CSV_PATH,
) -> None:
    sheet = xlrd.open_workbook(xls_path).sheet_by_index(0)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row_num in range(sheet.nrows):
            writer.writerow(map(cell_to_str, sheet.row_values(row_num)))
    print(f"{xls_path} -> {csv_path}: строк данных {sheet.nrows - 1}")
