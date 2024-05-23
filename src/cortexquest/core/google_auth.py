from pathlib import Path
from typing import Union

import gspread
from google.oauth2.service_account import Credentials


class GoogleAuth:
    def __init__(self, credentials_file: Union[str, Path]):
        self.credentials_file = Path(credentials_file)
        self.client = None

    def authenticate(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_file(
            self.credentials_file, scopes=scopes
        )
        self.client = gspread.authorize(credentials)

    def get_client(self):
        if not self.client:
            self.authenticate()
        return self.client
