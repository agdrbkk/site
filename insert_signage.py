import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def insert_signage_tasks():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # แทรกที่ Row 13, 14, 15 (ต่อจาก 1.8)
    values = [
        ["1.9", "งานป้ายไฟหน้าร้าน", "ชุด", "1", "6000", "=D13*E13"],
        ["1.10", "งานป้ายไฟในร้าน / ป้ายเมนู", "ชุด", "1", "20000", "=D14*E14"],
        ["1.11", "งานสติ๊กเกอร์ตกแต่งภายในร้าน (เหมา)", "เหมา", "1", "30000", "=D15*E15"]
    ]
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A13:F15", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: เพิ่มรายการป้ายและสติ๊กเกอร์ (1.9 - 1.11) เรียบร้อย")

if __name__ == '__main__':
    insert_signage_tasks()
