import pandas as pd
import numpy as np
pd.set_option("future.no_silent_downcasting", True)

REPLACE_DICT = {
    "כלל לא": 0,
    "מספר ימים": 1,
    "ביותר ממחצית מן הימים": 2,
    "כמעט כל יום": 3,
    "": np.nan
}


class GAD7Translator:
    def __init__(self, data:pd.DataFrame):
        self.data = data
    
    def _collect_gad7_questionnaire(self) -> pd.DataFrame:
        gad7_tab = self.data.filter(regex="MH-GAD").copy()
        gad7_tab.columns = range(len(gad7_tab.columns))
        gad7_tab = gad7_tab.iloc[:, :7]
        gad7_tab.columns = range(7)
        gad7_tab = gad7_tab.replace(REPLACE_DICT)
        return gad7_tab

    @staticmethod
    def calculate_gad7(row: pd.Series) -> float:
        """
        Calculate the GAD7 scores from the questionnaire data.

        Parameters
        ----------
        data : pd.Series
            A pandas Series containing the questionnaire data.

        Returns
        -------
        float
            The GAD7 score for the questionnaire data.
        """
        if row.isna().any():
            return np.nan
        return row.astype(int).sum()
