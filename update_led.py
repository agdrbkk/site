import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def update_led_price():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:B100").execute()
    rows = result.get('values', [])
    
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0] == "3.4":
            # อัปเดตราคาเหมา
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'{sheet_name}'!C{i+1}:E{i+1}", 
                valueInputOption='USER_ENTERED',
                body={'values': [["เหมา", "1", "8000"]]}
            ).execute()
            break
    
    print(f"SUCCESS: อัปเดตราคา LED Strip Light เป็นเหมา 8000 เรียบร้อย")

if __name__ == '__main__':
    update_led_price()
