import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_tile_wall_task():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # แทรกหลังจาก 1.4 (Row 8, index 7)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])
    
    new_rows = []
    inserted = False
    for i, row in enumerate(rows):
        if i == 8:
            new_rows.append(["1.5", "งานกรุกระเบื้องผนัง 60x60 ซม. (ราคากระเบื้องไม่เกิน 300.-/ตร.ม.)", "ตร.ม.", "6.5", "3300"])
            inserted = True
        
        if inserted and len(row) > 0 and "." in row[0]:
            parts = row[0].split('.')
            if parts[0] == "1" and int(parts[1]) >= 5:
                row[0] = f"1.{int(parts[1])+1}"
        
        new_rows.append(row)

    body = {'values': new_rows}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: เพิ่มรายการ 1.5 (กรุกระเบื้องผนัง) เรียบร้อย")

if __name__ == '__main__':
    update_tile_wall_task()
