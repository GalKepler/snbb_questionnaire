from pathlib import Path
from typing import Optional, Union

import pandas as pd

from cortexquest.core.google_auth import GoogleAuth
from cortexquest.core.translators import headers


class SheetLoader:
    """
    A class to load data from a Google Sheet.
    """

    def __init__(self, sheet_url: str, credentials_file: Union[str, Path]):
        """
        Initialize the SheetLoader object.

        Parameters
        ----------
        sheet_url : str
            The URL of the Google Sheet to load.
        credentials_file : Union[str, Path]
            The path to the Google service account credentials file.
        """
        self.sheet_url = sheet_url
        self.credentials_file = Path(credentials_file)
        self.client = None
        self._sheet_data = None

    def authenticate(self):
        """
        Authenticate with Google Sheets.
        """
        google_auth = GoogleAuth(self.credentials_file)
        self.client = google_auth.get_client()

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the Google Sheet.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the data from the Google Sheet.
        """
        if self._sheet_data is not None:
            return self._sheet_data
        if not self.client:
            self.authenticate()
        sheet = self.client.open_by_url(self.sheet_url)
        worksheet = sheet.get_worksheet(0)  # Assumes the first worksheet
        sheet_data = pd.DataFrame(worksheet.get_all_records())
        sheet_data.columns = (
            sheet_data.columns.str.replace('"', "'")
            .str.strip()
            .str.replace(" ]", "]")
            .str.replace(" ?", "?")
        )
        sheet_data = sheet_data.rename(columns=headers)
        self._sheet_data = sheet_data
        return sheet_data

    @property
    def sheet_data(self) -> Optional[pd.DataFrame]:
        """
        Get the loaded sheet data.

        Returns
        -------
        Optional[pd.DataFrame]
            The loaded sheet data as a pandas DataFrame.
        """
        return self.load_data() if self._sheet_data is None else self._sheet_data
