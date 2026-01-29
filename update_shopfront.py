import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_shopfront_task():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ดึงข้อมูลมาเพื่อจัดลำดับใหม่
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])
    
    new_rows = []
    inserted = False
    for i, row in enumerate(rows):
        # แทรกหลังจาก 1.3 (Row 7, index 6)
        if i == 7:
            new_rows.append(["1.4", "งานผนังตกแต่งหน้าร้าน (วัสดุผสม ลามิเนต/WPC/ป้ายไฟ)", "ตร.ม.", "15", "8000"])
            inserted = True
        
        # ขยับลำดับข้ออื่นในหมวด 1
        if inserted and len(row) > 0 and "." in row[0]:
            parts = row[0].split('.')
            if parts[0] == "1" and int(parts[1]) >= 4:
                row[0] = f"1.{int(parts[1])+1}"
        
        new_rows.append(row)

    body = {'values': new_rows}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: เพิ่มรายการ 1.4 (ผนังหน้าร้าน) เรียบร้อยแล้ว")

if __name__ == '__main__':
    update_shopfront_task()
