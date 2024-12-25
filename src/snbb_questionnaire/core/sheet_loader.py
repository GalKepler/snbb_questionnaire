from pathlib import Path
from typing import Optional, Union

import pandas as pd
import gspread as gs
from snbb_questionnaire.core.translators import headers


class SheetLoader:
    """
    A class to load data from a Google Sheet.
    """

    DATA_SHEET_NUMBER = 1
    METADATA_SHEET_NUMBER = 0

    def __init__(self, sheet_key: str):
        """
        Initialize the SheetLoader object.

        Parameters
        ----------
        sheet_key : str
            The key of the Google Sheet.
        credentials_file : Union[str, Path]
            The path to the Google service account credentials file.
        """
        self.sheet_key = sheet_key
        self._sheet = None
        self._sheet_data = None
        self._auth = None

    def __authenticate(self):
        """
        Authenticate the Google client.
        """
        return gs.oauth()

    def _read_sheet(self) -> pd.DataFrame:
        """
        Read the Google Sheet data.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the data from the Google Sheet.
        """
        if not self._auth:
            self._auth = self.__authenticate()
        sheet = self._auth.open_by_key(self.sheet_key)
        self._sheet = sheet
        return sheet

    def load_data(self) -> pd.DataFrame:
        """
        Load metadata from the Google Sheet.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the metadata from the Google Sheet.
        """
        worksheet = self.sheet.get_worksheet(
            self.DATA_SHEET_NUMBER
        )  # Assumes the first worksheet
        data = worksheet.get_all_values()
        sheet_data = pd.DataFrame(data[1:], columns=data[0])
        self._sheet_data = sheet_data

        return sheet_data.rename({"": "questionnaire_id"}, axis=1)

    def load_metadata(self) -> pd.DataFrame:
        """
        Load data from the Google Sheet.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the data from the Google Sheet.
        """
        worksheet = self.sheet.get_worksheet(self.METADATA_SHEET_NUMBER)
        data = worksheet.get_all_values()
        sheet_data = pd.DataFrame(data[1:], columns=data[0])
        sheet_data["question_english"] = sheet_data["Question"].apply(
            lambda x: self.translate(x)
        )
        self._metadata = sheet_data
        return sheet_data

    @staticmethod
    def translate(x):
        result = headers.get(x)
        if not result:
            key1 = x.split(".")[0]
            key2 = "[" + x.split("[")[-1]
            result = headers.get((key1, key2))
        return result

    @property
    def sheet(self) -> gs.Spreadsheet:
        """
        Get the loaded sheet.

        Returns
        -------
        gs.Spreadsheet
            The loaded sheet.
        """
        return self._read_sheet() if self._sheet is None else self._sheet

    @property
    def metadata(self) -> Optional[pd.DataFrame]:
        """
        Get the loaded metadata.

        Returns
        -------
        Optional[pd.DataFrame]
            The loaded metadata as a pandas DataFrame.
        """
        return self.load_metadata() if self._metadata is None else self._metadata

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
