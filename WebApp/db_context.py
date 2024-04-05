import csv
import os
from pathlib import Path

class DBContext:
    data_path: str

    def __init__(self, data_path: str):
        self.data_path = "./"

    def read_from_csv(self, file_name: str):
        with open(file_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return list(csv_reader)

    def write_to_csv(self, file_name: str, data: list[object], headers: list[str]):
        if len(data) > 0:
            with open(file_name, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file,fieldnames=headers)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)