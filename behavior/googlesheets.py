from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

class Sheets:
    GOOGLE_KEY_FILE = 'calla_bot.json'
    def __init__(self, id):
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            ]


        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(Sheets.GOOGLE_KEY_FILE, self.scope)
        self.gc = gspread.authorize(self.credentials)

        self.workbook_key = id
        self.workbook = self.gc.open_by_key(self.workbook_key)
    def get_row(self, worksheet_index, row_index):
        sheet = self.workbook.get_worksheet(worksheet_index)
        value = sheet.get_all_values()
        return value[row_index]
    def get_color(self, category):
        if category == 'Design':
            return 16711680
        elif category == 'Groupbuy':
            return 16734483
        elif category == 'Misc.':
            return 5177599

if __name__ == '__main__':
    s = Sheets('1dD4QSbrBYBxJfmBSrPmv0h0tP35393vytqnkWBa45fE')
    print(s.get_row(0, 1))
    