import gspread
import pandas as pd

gc = gspread.oauth()

sh = gc.create('A new spreadsheet')

worksheet = sh.get_worksheet(0)

val = worksheet.acell('B1').value

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

worksheet.update([df.columns.values.tolist()] + df.values.tolist())
