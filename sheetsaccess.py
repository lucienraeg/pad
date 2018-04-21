import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
LOCAL_CLIENT_SECRET_DIR = WORKING_DIR + '/client_secret.json'

# access google sheets 
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(LOCAL_CLIENT_SECRET_DIR, scope)
client = gspread.authorize(creds)

def load_sheet():
	# load pad data from sheet
	sheet = client.open('pad-data').sheet1
	pad_data = []
	i = 1
	while True:
		row = sheet.row_values(i)
		if row == []:
			break
		else:
			pad_data.append(row)
			i += 1

	return sheet, pad_data

def update_sheet(sheet, entries):
	for i, entry in enumerate(entries):
		sheet.update_cell(i+1, 1, entry[0])
		sheet.update_cell(i+1, 2, entry[1])