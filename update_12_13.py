import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_tasks_12_13():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # 1. อัปเดต 1.2 (Row 6) และ 1.3 (Row 7)
    # Column A=ลำดับ, B=รายการ, C=หน่วย, D=ปริมาณ, E=ราคา
    values = [
        ["1.2", "งานกั้นผนังเคาน์เตอร์กรุไม้ HMR และคิ้วตกแต่ง (คิด 2 ด้าน)", "ตร.ม.", "9.5", "3000"],
        ["1.3", "งานกระจกอลูมิเนียม (ส่วนช่องออกอาหารและโชว์วัตถุดิบ)", "ตร.ม.", "6.5", "3500"]
    ]
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A6:E7", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: อัปเดตรายการ 1.2 และ 1.3 เรียบร้อยแล้ว")

if __name__ == '__main__':
    update_tasks_12_13()
