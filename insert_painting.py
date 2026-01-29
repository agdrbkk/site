import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def insert_painting_tasks():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # แทรกที่ Row 11 และ 12 (ต่อจาก 1.6)
    # เราจะเขียนทับเนื้อหาเดิมที่ติดมากับ template ด้วย
    values = [
        ["1.7", "ค่าแรงทาสีภายใน (ผนังและฝ้าเพดาน)", "ตร.ม.", "145", "150", "=D11*E11"],
        ["1.8", "ค่าสีทาภายใน (สีน้ำอะคริลิคเกรดพรีเมียม)", "ถัง", "5", "2500", "=D12*E12"]
    ]
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A11:F12", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: เพิ่มรายการ 1.7 (ค่าแรง) และ 1.8 (ค่าสี) เรียบร้อย")

if __name__ == '__main__':
    insert_painting_tasks()
