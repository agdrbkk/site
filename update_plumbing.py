import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_plumbing_price():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:B100").execute()
    rows = result.get('values', [])
    
    # หา Row ที่เป็น "5" (หัวข้อหมวด)
    plumbing_header_row = None
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] == "5":
            plumbing_header_row = i + 1
            break

    # หยอดราคาและข้อมูลใหม่ลงไป
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!C{plumbing_header_row+1}:E{plumbing_header_row+1}",
        valueInputOption='USER_ENTERED',
        body={'values': [["ชุด", "1", "6000"]]}
    ).execute()
    
    print(f"SUCCESS: อัปเดตงานประปาเป็นเหมา 6000 บาท เรียบร้อย")

if __name__ == '__main__':
    update_plumbing_price()
