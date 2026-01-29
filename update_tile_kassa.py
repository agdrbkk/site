import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_tile_to_kassa():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    tile_url = "https://www.thaiwatsadu.com/th/product/กระเบื้องผนัง-DIGITAL-KASSA-รุ่น-KS-INW100-มิลกี้-ขนาด-30-x-60-ซม-60302368"
    
    # อัปเดตรายการ 1.5 (Row 9)
    # Column B=ชื่อ, D=ปริมาณ, E=ราคา, G=หมายเหตุ
    values = [
        ["งานกรุกระเบื้องผนัง (ราคากระเบื้องไม่เกิน 360.-/ตร.ม.)", "ตร.ม.", "6.5", "3360"]
    ]
    
    # อัปเดตข้อมูลหลัก
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!B9:E9", 
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()
    
    # อัปเดตหมายเหตุ (G9)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!G9", 
        valueInputOption='USER_ENTERED',
        body={'values': [[tile_url]]}
    ).execute()
    
    print(f"SUCCESS: อัปเดตรายการ 1.5 เป็นกระเบื้อง KASSA @ 360.- เรียบร้อย")

if __name__ == '__main__':
    update_tile_to_kassa()
