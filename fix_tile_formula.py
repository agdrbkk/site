import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def fix_tile_price_formula():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # 1. แก้ไขราคาต่อหน่วย (Column E) ให้เหลือแค่ค่าของ 360
    # 2. แก้ไขสูตรในช่องรวมราคา (Column F) ให้บวกค่าแรง 3000
    
    # อัปเดต Column E (ราคาต่อหน่วย)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!E9", 
        valueInputOption='USER_ENTERED',
        body={'values': [["360"]]}
    ).execute()
    
    # อัปเดต Column F (สูตรใหม่)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!F9", 
        valueInputOption='USER_ENTERED',
        body={'values': [["=(D9*E9)+3000"]]}
    ).execute()
    
    print(f"SUCCESS: แก้ไขวิธีคิดราคาข้อ 1.5 (ค่าของ 360 + ค่าแรงคงที่ 3000) เรียบร้อย")

if __name__ == '__main__':
    fix_tile_price_formula()
