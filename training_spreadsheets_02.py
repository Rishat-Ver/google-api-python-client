import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv


load_dotenv()

SECRET_FILE = os.getenv("SECRET_FILE")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def auth():
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    sheets = build("sheets", "v4", credentials=creds)
    drive = build("drive", "v3", credentials=creds)
    return sheets, drive, creds


def create_spreadsheet(sheets):
    spreadsheet_body = {
        "properties": {"title": "Бюджет путешествий02", "locale": "ru_RU"},
        "sheets": [{
            "properties": {
                "sheetType": "GRID",
                "sheetId": 0,
                "title": "Отпуск 2077",
                "gridProperties": {"rowCount": 100, "columnCount": 100}
            }
        }]
    }
    resp = sheets.spreadsheets().create(body=spreadsheet_body).execute()
    spreadsheet_id = resp["spreadsheetId"]
    print(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    return spreadsheet_id


def set_user_permissions(drive, spreadsheet_id, email, role="writer"):
    drive.permissions().create(
        fileId=spreadsheet_id,
        body={"type": "user", "role": role, "emailAddress": email},
        fields="id",
        sendNotificationEmail=True
    ).execute()


def write_test(sheets, spreadsheet_id):
    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Отпуск 2077",
        valueInputOption="RAW",
        body={"values": [["TEST"]]}
    ).execute()


if __name__ == "__main__":
    sheets, drive, creds = auth()
    spreadsheet_id = create_spreadsheet(sheets)

    # set_user_permissions(drive, spreadsheet_id,
    #     "rishatpracticum@authentic-ether-469312-j6.iam.gserviceaccount.com")

    write_test(sheets, spreadsheet_id)
    print("OK")
