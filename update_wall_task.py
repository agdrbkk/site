import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_wall_construction():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ข้อมูลที่จะอัปเดตแทนที่ข้อ 1.1 (Row 5)
    # Column A=ลำดับ, B=รายการ, C=หน่วย, D=ปริมาณ, E=ราคาต่อหน่วย, F=ราคารวม
    values = [
        ["1.1", "งานก่อผนังเบาสมาร์ทบอร์ด (โครงคร่าวสังกะสี)", "ตร.ม.", "16", "2000", "32000"]
    ]
    
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A5", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: อัปเดตงานก่อผนังเบาเรียบร้อย (16 ตร.ม. @ 2000 บาท)")

if __name__ == '__main__':
    update_wall_construction()
