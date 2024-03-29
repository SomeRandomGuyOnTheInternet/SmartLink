import csv

class DBContext:
	data_path: str

	def __init__(self, data_path):
		self.data_path = data_path

	def read_from_csv(self, file_name: str):
		with open(self.data_path + file_name, mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			return csv_reader

	def write_to_csv(self, file_name: str, headers: list, data: list):
		with open(self.data_path + file_name, mode='w') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=headers)
			writer.writeheader()
			for row in data:
  				writer.writerow(row)