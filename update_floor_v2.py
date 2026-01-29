import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_floor_detailed():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ดึงตำแหน่ง Row ของหมวด 2 อีกที
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:A50").execute()
    rows = result.get('values', [])
    
    floor_header_row = 0
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] == "2":
            floor_header_row = i + 1
            break
            
    if floor_header_row == 0: floor_header_row = 17

    # หยอดข้อมูล 2.1 และ 2.2
    values = [
        ["2.1", "ค่าแรงปูกระเบื้องพื้น (รวมวัสดุปูนกาว/ทราย/ยาแนว)", "ตร.ม.", "53", "550", f"=D{floor_header_row+1}*E{floor_header_row+1}"],
        ["2.2", "ค่ากระเบื้องพื้น 60x60 ซม. (1 กล่องมี 4 แผ่น)", "กล่อง", "13", "357", f"=D{floor_header_row+2}*E{floor_header_row+2}"]
    ]
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A{floor_header_row + 1}", 
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()
    
    print(f"SUCCESS: อัปเดตงานพื้นแบบแยกรายการ (2.1, 2.2) เรียบร้อย")

if __name__ == '__main__':
    update_floor_detailed()
