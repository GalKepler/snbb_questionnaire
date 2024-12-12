"""Main module."""

"""Main module."""

import pandas as pd
from snbb_questionnaire.core.sheet_loader import SheetLoader
from snbb_questionnaire.core.translators.psqi import PSQI


class SnbbQuestionnaire:
    """
    A class to represent a questionnaire for the SNBB project.
    """

    def __init__(self, sheet_key: str):
        """
        Parameters
        ----------
        sheet_key : str
            The key of the Google Sheet containing the questionnaire data.

        Attributes
        ----------
        _sheet_loader : SheetLoader
            A SheetLoader object to load the questionnaire data.
        _metadata : pd.DataFrame
            A pandas DataFrame containing the metadata for the questionnaire.
        _raw_data : pd.DataFrame
            A pandas DataFrame containing the raw data from the Google Sheet.
        _data : pd.DataFrame
            A pandas DataFrame containing the data for the questionnaire
        """
        self._sheet_loader: SheetLoader = SheetLoader(sheet_key)
        self._metadata: pd.DataFrame = None
        self._raw_data: pd.DataFrame = self._sheet_loader.sheet_data
        self._data: pd.DataFrame = None

    def load_data(self):
        """
        Load the questionnaire data from the Google Sheet.
        """
        psqi = PSQI(self._raw_data)
        for i, row in self._data.iterrows():
            res = psqi.psqi_score(row)
            for key, value in res.items():
                self.data.at[i, key] = value

    @property
    def metadata(self):
        """
        Get the metadata for the questionnaire.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the metadata.
        """
        return self._metadata

    @property
    def data(self):
        """
        Get the data for the questionnaire.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the data.
        """
        if not self._data:
            self.load_data()
        return self._data
