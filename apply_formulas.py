import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def formula_link():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1a8GoEmuLzGHsqfYd8FuWGB5Ycq8kIt1RXV7Yfliz1lA'
    sheet_name = 'ฟู่เฉิง Go Wholesale'
    
    # สร้างลิสต์สูตรสำหรับ Column F (Row 5 ถึง 30)
    # ใน Sheets สูตรคือ =D5*E5, =D6*E6, ...
    formulas = []
    for i in range(5, 31):
        formulas.append([f"=D{i}*E{i}"])
    
    body = {'values': formulas}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!F5:F30", 
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"SUCCESS: ผูกสูตร Column F เรียบร้อยแล้ว (แถว 5-30)")

if __name__ == '__main__':
    formula_link()
