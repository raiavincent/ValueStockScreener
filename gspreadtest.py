import gspread
import pandas as pd

gc = gspread.oauth()

# sh = gc.create('A new spreadsheet',folder_id='place folder ID here')

sh1 = gc.open_by_url('place url here')

worksheet = sh1.get_worksheet(0)

val = worksheet.acell('B1').value

# worksheet = sh.get_worksheet(0)

# val = worksheet.acell('B1').value

# d = {'col1': [1, 2], 'col2': [3, 4]}
# df = pd.DataFrame(data=d)

# worksheet.update([df.columns.values.tolist()] + df.values.tolist())
