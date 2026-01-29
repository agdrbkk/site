import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_tile_remark():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ลิงก์กระเบื้องบุญถาวร
    tile_url = "https://www.boonthavorn.com/sosuco-1226062"
    
    # รายการ 1.5 อยู่ที่ Row 9 ใน Sheet (หลังจากแทรกไปมา)
    # เราจะแปะลิงก์ไว้ที่ Column G (หมายเหตุ)
    body = {'values': [[tile_url]]}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!G9", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: แปะลิงก์กระเบื้องในหมายเหตุข้อ 1.5 เรียบร้อยแล้ว")

if __name__ == '__main__':
    update_tile_remark()
