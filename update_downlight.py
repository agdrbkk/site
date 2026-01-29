import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_downlight_count():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # อัปเดตปริมาณดาวน์ไลท์ (3.2) เป็น 32 จุด
    # นับจากหัว Sheet, Row ที่ 11 คือ 3.2 (งานดาวน์ไลท์)
    values = [["32"]]
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!D12", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: อัปเดตจำนวนดาวน์ไลท์เป็น 32 จุด เรียบร้อย")

if __name__ == '__main__':
    update_downlight_count()
