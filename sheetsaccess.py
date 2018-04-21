import gspread
from oauth2client.service_account import ServiceAccountCredentials

# access google sheets 
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
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