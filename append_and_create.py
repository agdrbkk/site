import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from get_sheet_info import get_sheet_info

def append_data(spreadsheet_id, sheet_name, data, sheet_id=None):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    body = {'values': data}

    # Use the sheet_id if it's provided.
    if sheet_id:
        range_str = f"'{sheet_name}'!A1" # Append function cannot use sheet ID
    else:
        range_str = f"'{sheet_name}'!A1:append"

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_str,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()


def create_sheet(spreadsheet_id, sheet_name):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]
    }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        sheet_id = response.get('replies')[0]['addSheet']['properties']['sheetId']
        print(f"Successfully created the sheet {sheet_name} with id {sheet_id}")
        return sheet_id
    except Exception as e:
        print(f"Failed to create the sheet{sheet_name} due to {e}")
        return None