import csv
import datetime

can_connect = True
try:
	import sheetsaccess
	print('Server: Successfully connected to server')
except:
	can_connect = False
	print('Server: Cannot connect to server')


def local_save(entries):
	with open('local-pad-data.csv', 'w', newline='') as file:
		writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for entry in entries:
			writer.writerow(entry)
			# date_str = datetime.datetime.now().strftime('%d-%m-%Y')

def local_load():
	lines = []
	with open('local-pad-data.csv', newline='') as file:
		reader = csv.reader(file, delimiter=',', quotechar='|')
		for entry in reader:
			lines.append(entry)
	return lines

if __name__ == '__main__':
	# access sheet
	if can_connect:
		sheet, pad_data = sheetsaccess.load_sheet()

		# update local copy
		local_pad_data = local_load()

		if not local_pad_data == pad_data:
			print('Client: Updating local copy')
			local_save(pad_data)
		print('Client: Local copy is up-to-date')
		
	else:
		print('Client: Accessing local copy')
		pad_data = local_load()