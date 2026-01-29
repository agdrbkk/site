import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_hmr_task_v3():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # อัปเดตรายการ 1.2 (Row 6)
    # Column B=รายการ, C=หน่วย, D=ปริมาณ, E=ราคา
    values = [
        ["งานกั้นผนังเคาน์เตอร์กรุไม้ HMR และคิ้วตกแต่ง (คิด 2 ด้าน)", "ตร.ม.", "9.5", "5000"]
    ]
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!B6:E6", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: อัปเดตงานกรุไม้ HMR เป็น 9.5 ตร.ม. (2 ด้าน) เรียบร้อย")

if __name__ == '__main__':
    update_hmr_task_v3()
