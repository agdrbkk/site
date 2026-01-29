import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_paint_area():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # อัปเดตปริมาณงานทาสี (รายการ 1.3)
    # ในข้อมูลเดิม รายการ 1.3 อยู่ที่แถวที่ 7 ของ boq_data ซึ่งหยอดเริ่มที่ B5 
    # ดังนั้น 1.3 จะอยู่ที่แถวที่ 9 (Row 9) ใน Sheet
    # Column A=ลำดับ, B=รายการ, C=หน่วย, D=ปริมาณ
    
    body = {'values': [["96"]]}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!D9", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: อัปเดตพื้นที่ทาสีเป็น 96 ตร.ม. เรียบร้อยแล้ว")

if __name__ == '__main__':
    update_paint_area()
