import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_floor_task():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # หยอดข้อมูลหมวด 2 เริ่มที่ Row 17 (สมมติว่า Row 16 เป็นหัวข้อหมวด 2)
    # เราต้องเช็คแถวที่แน่นอนอีกทีเพื่อให้งานพื้นอยู่ถูกหมวด
    
    # ดึงข้อมูลมาดูตำแหน่งหมวด 2
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:A50").execute()
    rows = result.get('values', [])
    
    floor_header_row = 0
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] == "2":
            floor_header_row = i + 1
            break
            
    if floor_header_row == 0: floor_header_row = 17 # fallback

    values = [
        ["2.1", "งานปูกระเบื้องพื้น (60x60 ซม.) ทั่วบริเวณ (ค่ากระเบื้อง 247.92.-/ตร.ม.)", "ตร.ม.", "53", "647.92", "=D" + str(floor_header_row + 1) + "*E" + str(floor_header_row + 1)]
    ]
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A{floor_header_row + 1}", 
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()
    
    print(f"SUCCESS: อัปเดตงานปูกระเบื้องพื้น (2.1) เรียบร้อย")

if __name__ == '__main__':
    update_floor_task()
