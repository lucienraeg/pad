import csv
import datetime
import sys
import os

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
LOCAL_PAD_DATA_DIR = WORKING_DIR + '/local-pad-data.csv'

can_connect = False

# if 'offline' is not typed after
if len(sys.argv) == 1:
	try:
		import sheetsaccess
		print('Server: Successfully connected to server')
		can_connect = True
	except:
		print('Server: Server connection unsuccesful')


def local_save(entries):
	with open(LOCAL_PAD_DATA_DIR, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for entry in entries:
			writer.writerow(entry)

def local_load():
	lines = []
	with open(LOCAL_PAD_DATA_DIR, newline='') as file:
		reader = csv.reader(file, delimiter=',', quotechar='|')
		for entry in reader:
			lines.append(entry)
	return lines

def print_commands():
	print("Commands:")
	print("- 'add [text]'                adds an entry")
	print("- 'insert [index] [text]'     rewrites an entry")
	print("- 'remove [index]'            removes an entry")
	print("- 'show [index](optional)'    shows an entry" )
	print("- 'help'                      shows this message" )
	print("- 'exit'                      exits pad" )

def main():
	user_input = input("User: ")
	prefix = user_input.split()[0]
	msg = " ".join(user_input.split()[1:])

	if prefix == 'add':
		if not msg == '':
			
			date = datetime.datetime.now().strftime("%d-%m-%Y")
			pad_data.append([date, msg])

			# update data files
			local_save(pad_data)
			if can_connect:
				sheet.update_cell(len(pad_data), 1, date)
				sheet.update_cell(len(pad_data), 2, msg)

			print("")
			print("Added entry [{}]".format(date))
			print("")
		else:
			print("Error: Command 'add' requires a message")
	elif prefix == 'insert':
		i = None
		try:
			i = int(msg.split()[0])
			m = " ".join(msg.split()[1:])

			pad_data[i][1] = m

			# update data files
			local_save(pad_data)
			if can_connect:
				sheet.update_cell(i+1, 2, m)

			print("")
			print("Rewrote entry [{}]".format(pad_data[i][0]))
			print("")
		except IndexError:
			print("Error: Index '{}' out of range".format(i))
		except ValueError:
			print("Error: Command 'remove' requires an integer index")
	elif prefix == 'remove':
		try:
			i = int(msg)

			pad_data[i][1] = ''
			# update data files
			local_save(pad_data)
			if can_connect:
				sheet.update_cell(i+1, 2, '')

			print("")
			print("Removed entry [{}]".format(pad_data[i][0]))
			print("")
		except IndexError:
			print("Error: Index '{}' out of range".format(i))
		except ValueError:
			print("Error: Command 'remove' requires an integer index")
	elif prefix == 'show':
		if msg == "":
			# print all entries
			print("")
			for i, entry in enumerate(pad_data):
				print("{}. [{}]: {}".format(i, entry[0], entry[1]))
			print("")
		else:
			# print specific entry
			try:
				i = int(msg)
				try:
					print("")
					print("{}. [{}]: {}".format(i, pad_data[i][0], pad_data[i][1]))
					print("")
				except IndexError:
					print("Error: Index '{}' out of range".format(i))
			except ValueError:
				print("Error: Command 'show' requires an integer index")
	elif prefix == 'help':
		print_commands()
	elif prefix == 'exit':
		sys.exit()
	else:
		print("Error: Command '{}' unknown. Use 'help' for a list of commands".format(prefix))
		
if __name__ == '__main__':
	# access sheet
	if can_connect:
		sheet, pad_data = sheetsaccess.load_sheet()

		local_pad_data = local_load()

		# sync up local and server copies
		if len(pad_data) > len(local_pad_data):
			print('Client: Updating local copy (+{} entries)...'.format(len(pad_data)-len(local_pad_data)))
			local_save(pad_data)
			print('Client: Success')
		elif len(local_pad_data) > len(pad_data):
			print('Server: Updating server copy (+{} entries)...'.format(len(local_pad_data)-len(pad_data)))
			sheetsaccess.update_sheet(sheet, local_pad_data)
			print('Server: Success')
		else:
			print('Client: Everything up-to-date')
			pad_data = local_pad_data
	else:
		print('Client: Accessing local copy')
		pad_data = local_load()

	# main loop
	while True:
		main()