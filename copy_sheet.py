import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from get_sheet_info import get_sheet_info
from append_and_create import append_data, create_sheet

def copy_and_inflate():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'

    # 1. Get all the values from  the sheet
    rows, _ = get_sheet_info(spreadsheet_id, sheet_name)

    if rows is None:
      print("error in getting sheet info")
      return

    # 2. create the new sheet
    new_sheet_name = "ฟู่เฉิง Go Wholesale + 40% v2"
    new_sheet_id = create_sheet(spreadsheet_id, new_sheet_name)
    if new_sheet_id is None:
        print("error in creating sheet")
        return

    # 3 . Build the new data
    new_rows = []
    # spacer
    new_rows.append([""])
    new_rows.append([""])

    # Header
    new_rows.append(["(ปรับราคา +40%)", "", "", "", "", ""])
    new_rows.append(rows[2])  # copy the main header from original

    # Loop through each item in the original row for price inflating
    for i, row in enumerate(rows):
        if i > 3:  # skip headers
            new_row = row[:]
            try:  # check if numberable
                original_price = float(row[4])  # Column E contains price per unit
                inflated_price = original_price * 1.4
                new_row[4] = str(round(inflated_price, 2))  # Keep prices up to 2 decimals
                # update formula for new price since the column is duplicated too.
                new_row[5] = f"=D{i + 4}*E{i + 4}"  # check total number and add offset correctly
            except Exception as e:
                pass  # leave as is because we are not updating the number, string etc
            new_rows.append(new_row)

    # 4. Append all the data to the sheet
    append_data(spreadsheet_id, new_sheet_name, new_rows, new_sheet_id)

    print(f"SUCCESS: สร้างตารางใหม่ (ปรับราคา 40%) สำเร็จแล้ว")

if __name__ == '__main__':
    copy_and_inflate()
