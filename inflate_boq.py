import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def copy_and_inflate():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'

    # 1. อ่านข้อมูลทั้งหมดในตาราง
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])

    # 2. เตรียมข้อมูลใหม่ (ปรับราคา 40%)
    new_rows = []
    # เว้นบรรทัดห่างๆ หน่อย
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

    # 3. เขียนข้อมูลใหม่ต่อท้าย ( append ) ท้ายของ Sheet
    body = {'valueInputOption': 'USER_ENTERED', 'values': new_rows}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1:append",  # append mode does not care about index;  new rows are simply added
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    print(f"SUCCESS: สร้างตารางใหม่ (ปรับราคา 40%) สำเร็จแล้ว")

if __name__ == '__main__':
    copy_and_inflate()
