import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_electric_prices():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # ดึงข้อมูลมาหาตำแหน่ง Row อีกที
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:B100").execute()
    rows = result.get('values', [])
    
    updates = []
    for i, row in enumerate(rows):
        if len(row) > 0:
            if row[0] == "3.1":
                updates.append({'range': f"'{sheet_name}'!B{i+1}:E{i+1}", 'values': [["ตู้เมน (เพิ่มลูกเซอร์กิต)", "ชุด", "1", "5000"]]})
            elif row[0] == "3.2":
                updates.append({'range': f"'{sheet_name}'!E{i+1}", 'values': [["550"]]})
            elif row[0] == "3.5":
                updates.append({'range': f"'{sheet_name}'!E{i+1}", 'values': [["550"]]})

    body = {'valueInputOption': 'USER_ENTERED', 'data': data}
    # อ๊ะ ลืมประกาศ data ตัวแปรเดียวกับ updates
    body = {'valueInputOption': 'USER_ENTERED', 'data': updates}
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    
    print(f"SUCCESS: อัปเดตราคาหมวดไฟฟ้า (3.1, 3.2, 3.5) เรียบร้อย")

if __name__ == '__main__':
    update_electric_prices()
