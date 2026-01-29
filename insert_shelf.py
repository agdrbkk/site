import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def insert_shelf_task():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # แทรกรายการต่อท้ายหมวด 1 (หาตำแหน่งสุดท้ายก่อน)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:B100").execute()
    rows = result.get('values', [])

    last_item_row = 0
    for i, row in enumerate(rows):
        if len(row) > 0 and (row[0].startswith("2") or row[0].startswith("3") or row[0].startswith("4") or row[0].startswith("5") or row[0].startswith("6")):
            last_item_row = i
            break # เจอหมวดใหม่แล้ว แปลว่าก่อนหน้าคือ item สุดท้าย
    
    # Insert new row
    insert_row_index = last_item_row  # แทรกก่อนหน้านี้

    requests = [{
                'insertText': {'objectId': service,'text':''}
            }]

    # Insert New code to google sheet

    values = [
        ["1.12", "ชั้นวางของ (ติดผนัง) - พร้อมโครงและติดตั้ง", "ชิ้น", "2", "2000", "=D"+str(insert_row_index+1)+"*E"+str(insert_row_index+1)]
    ]

    body = {'values': values}
    insert_range = f"'{sheet_name}'!A{insert_row_index+1}" # insert after the 1.11 = +1
    service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=insert_range,  
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

    print(f"SUCCESS: เพิ่ม 1.12 ชั้นวางของ = 4000 บาท เรียบร้อย.")

if __name__ == '__main__':
    insert_shelf_task()
