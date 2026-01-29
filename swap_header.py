import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def swap_electric_header():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ค้นหาหัวข้อเดิมและเปลี่ยนเลขหมวด
    # นีโอจะไปไล่แก้หัวข้อที่เคยเขียนไว้ว่าเป็น "4. งานระบบไฟฟ้า" ให้เป็น "3. งานระบบไฟฟ้า"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:B100").execute()
    rows = result.get('values', [])
    
    updates = []
    for i, row in enumerate(rows):
        if len(row) > 0:
            # ถ้าเป็นหัวข้อหมวด (ตัวเลขเดี่ยว)
            if row[0] == "4":
                updates.append({'range': f"'{sheet_name}'!A{i+1}", 'values': [["3"]]})
            # ถ้าเป็นรายการย่อย (เช่น 4.1, 4.2)
            elif row[0].startswith("4."):
                new_label = row[0].replace("4.", "3.", 1)
                updates.append({'range': f"'{sheet_name}'!A{i+1}", 'values': [[new_label]]})

    # ส่งคำสั่งอัปเดตแบบรวบยอด
    data = []
    for u in updates:
        data.append({'range': u['range'], 'values': u['values']})
        
    body = {'valueInputOption': 'USER_ENTERED', 'data': data}
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    
    print(f"SUCCESS: สลับหมวดไฟฟ้าเป็นหมวด 3 เรียบร้อย")

if __name__ == '__main__':
    swap_electric_header()
