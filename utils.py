import pandas as pd
import gspread
from data import sorted_dictionary
from tkinter import filedialog, ttk
from tkinter import *
from oauth2client.service_account import ServiceAccountCredentials

root = Tk()


def get_worksheets_names():
    with pd.ExcelFile('output.xlsx', engine='openpyxl') as xls:
        sheet_names = xls.sheet_names

    return sheet_names


def insert_data():
    sorted_dictionary()

    def insert_to_google_sheets(worksheet_name, spreadsheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)

        spreadsheet = client.open(spreadsheet_name)

        worksheet = spreadsheet.worksheet(worksheet_name)

        df = pd.read_excel('output.xlsx', sheet_name=worksheet_name)
        values = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(values)

    sheets_names = get_worksheets_names()
    for sheet_name in sheets_names:
        insert_to_google_sheets(sheet_name, 'Dictionary')


def load_data():
    input_text.delete(1.0, 'end')
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
            input_text.insert('end', data)


def generate_random_output():
    input_lines = input_text.get('1.0', END).split('\n')
    num_lines = int(number_entry.get())

    num_lines = len(input_lines) if num_lines > len(input_lines) else num_lines

    df = pd.read_excel('output.xlsx')
    selected_columns = df[['Слово', 'Часть речи', 'Лемма', 'Перевод']]
    random_rows = selected_columns.sample(n=num_lines)

    for index, row in random_rows.iterrows():
        row_str = ' // '.join([str(value) for value in row])
        output_text.insert('end', row_str + '\n')


number_frame = ttk.Frame(root)
number_entry = ttk.Entry(number_frame)
input_text = Text(root)
output_text = Text(root)
__all__ = ['root', 'input_text', 'output_text', 'number_frame', 'number_entry', 'load_data', 'insert_data',
           'generate_random_output']
