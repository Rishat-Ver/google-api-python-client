import os

from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from dotenv import load_dotenv


load_dotenv()


EMAIL = os.getenv("EMAIL")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]


def auth():
    credentials = Credentials.from_service_account_file(
        filename=CREDENTIALS_FILE, scopes=SCOPES
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    # print(credentials.service_account_email)
    return service, credentials


def create_spreadsheet(service):

    spreadsheet_body = {
        'properties': {
            'title': 'Бюджет путешествий',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Отпуск 2077',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 100
                }
             }
         }]
    }

    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheet_id = response['spreadsheetId']

    return spreadsheet_id


def set_user_permissions(spreadsheet_id, credentials):
    permissions_body={'type': 'user',
                      'role': 'writer',
                      'emailAddress': EMAIL}

    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permissions_body,
        fields='id'
    ).execute()


if __name__ == '__main__':
    service, credentials = auth()
    spreadsheetId = create_spreadsheet(service)
    set_user_permissions(spreadsheetId, credentials)
