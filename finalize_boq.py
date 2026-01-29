import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def finalize_boq():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # 1. หาแถวเริ่มต้นของหมวด 6 (งานแอร์/CCTV) เพื่อใช้เป็นจุดสิ้นสุดการใส่สูตร
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:B100").execute()
    rows = result.get('values', [])

    last_item_row = 0
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] == "6":
            last_item_row = i - 1  # แถวก่อนหน้าคือรายการสุดท้าย
            break
    if last_item_row == 0: last_item_row = len(rows) # fallback

    # 2. ใส่สูตรใน Column F ให้ครบ (ไล่ตั้งแต่แถว 5 ถึง last_item_row+1)
    formula_updates = []
    for i in range(5, last_item_row + 2):
        formula_updates.append({'range': f"'{sheet_name}'!F{i}", 'values': [[f"=D{i}*E{i}"]]})

    # 3. สร้างช่องราคารวมด้านล่าง
    total_row = last_item_row + 4 # เว้น 2 บรรทัด
    formula_range = f"F5:F{last_item_row+1}"  # เอา Row จากข้อ 1 มาใช้

    # เพิ่มข้อความ \"ราคารวมทั้งหมด\" และสูตร SUM
    footer_updates = [
        {'range': f"'{sheet_name}'!B{total_row}", 'values': [["ราคารวมทั้งหมด:"]]}
        ,
        {'range': f"'{sheet_name}'!F{total_row}", 'values': [["=SUM(" + formula_range + ")"]]}
    ]
    
    all_updates = formula_updates + footer_updates  # รวมทุกคำสั่ง

    body = {'valueInputOption': 'USER_ENTERED', 'data': []}
    body['data'] = all_updates # ต้องใส่ data แบบนี้ถึงจะ batch ได้
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    
    print(f"SUCCESS: ใส่สูตร Column F และคำนวณราคารวมทั้งหมดแล้ว")

if __name__ == '__main__':
    finalize_boq()
