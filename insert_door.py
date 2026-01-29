import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def insert_door_task():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ดึงข้อมูลมาเพื่อแทรกที่ Row 10 (ต่อจาก 1.5)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])
    
    new_rows = []
    inserted = False
    for i, row in enumerate(rows):
        if i == 9: # หลังจาก Row 9 (ซึ่งคือ 1.5)
            new_rows.append(["1.6", "งานติดตั้งประตูภายใน uPVC (ชุดประตูวงกบพร้อมลูกบิดมือจับ)", "บาน", "2", "7000", "=D10*E10"])
            inserted = True
        
        # ขยับลำดับข้ออื่นในหมวด 1 (ถ้ามี)
        if inserted and len(row) > 0 and "." in row[0]:
            parts = row[0].split('.')
            if parts[0] == "1" and int(parts[1]) >= 6:
                row[0] = f"1.{int(parts[1])+1}"
        
        new_rows.append(row)

    body = {'values': new_rows}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: แทรกรายการ 1.6 (ประตู uPVC) เรียบร้อย")

if __name__ == '__main__':
    insert_door_task()
