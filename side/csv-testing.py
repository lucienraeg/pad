import csv

def local_write_lines(lines):
	with open('notepad.csv', 'w', newline='') as file:
		writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for line in lines:
			writer.writerow([line])

def local_read_lines():
	lines = []
	with open('notepad.csv', newline='') as file:
		reader = csv.reader(file, delimiter=',' quotechar='|')
		for row in reader:
			lines.append(row[0])
	return lines



if __name__ == '__main__':
	a = ['john', 'steve', 'brian']
	local_write_lines(a)

	b = local_read_lines()
	print(b)