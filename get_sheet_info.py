import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_sheet_info(spreadsheet_id, sheet_name):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    # 1. Get the Sheet ID
    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet.get('sheets')
        sheet_id = None
        for sheet in sheets:
            if sheet['properties']['title'] == sheet_name:
                sheet_id = sheet['properties']['sheetId']
                break
        if sheet_id is None:
            print(f"Sheet with name {sheet_name} was not found")
            return None, None
        
    except Exception as e:
        print(f"Error getting sheet info: {e}")
        return None, None

    # 2. Get the values
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:F100").execute()
    rows = result.get('values', [])
    return rows, sheet_id