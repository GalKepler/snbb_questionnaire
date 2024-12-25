import pandas as pd

from enum import Enum

pd.set_option("future.no_silent_downcasting", True)

class BFI(Enum):
    AGREE = "Agreeableness"
    CONSC = "Conscientiousness"
    EXRTA = "Extraversion"
    NEURO = "Neuroticism"
    OPEN = "Openness to Experience"


BFI_QUESTIONS = {
    BFI.AGREE: [1, 6, 11, 16, 21, 26, 31, 36, 41],
    BFI.CONSC: [2, 7, 12, 17, 22, 27, 32, 37, 42],
    BFI.EXRTA: [0, 5, 10, 15, 20, 25, 30, 35],
    BFI.NEURO: [3, 8, 13, 18, 23, 28, 33, 38],
    BFI.OPEN: [4, 9, 14, 19, 24, 29, 34, 39, 40, 43],
}
REVERSED_SCORING = (1, 5, 7, 8, 11, 17, 20, 22, 23, 26, 30, 33, 34, 36, 40, 42)
REPLACE_DICT = {
    "בהחלט לא מסכים": 1,
    "בהחלט לא מסכים/ה": 1,
    "לא מסכים": 2,
    "לא מסכים/ה": 2,
    "ניטראלי": 3,
    "ניטראלי/ת": 3,
    "מסכים": 4,
    "מסכים/ה": 4,
    "מסכים בהחלט": 5,
    "מסכים/ה בהחלט": 5,
}

class BFITranslator:
    """
    A class to translate the BFI questionnaire data.

    Methods
    -------
    calculate_bfi(data: pd.Series) -> pd.Series
        Calculate the BFI scores from the questionnaire data.
    """

    def __init__(self, data:pd.DataFrame):
        self.data = data
    
    def _collect_bfi_questionnaire(self) -> pd.DataFrame:
        """
        Collect the BFI questionnaire data from the raw data.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the BFI questionnaire data.
        """
        bfi_tab = self.data.filter(regex="MH-BIG5").copy()
        bfi_tab.columns = range(len(bfi_tab.columns))
        bfi_tab = bfi_tab.replace(REPLACE_DICT).astype(int)
        return bfi_tab

    @staticmethod
    def calculate_bfi(row: pd.Series) -> pd.Series:
        """
        Calculate the BFI scores from the questionnaire data.

        Parameters
        ----------
        data : pd.Series
            A pandas Series containing the questionnaire data.

        Returns
        -------
        pd.Series
            A pandas Series containing the BFI
            scores for the questionnaire data.
        """
        scores = {}
        for trait in BFI:
            indices = BFI_QUESTIONS[trait]
            responses = row[indices]
            reverse = 6 - responses[responses.index.isin(REVERSED_SCORING)]
            responses.update(reverse)
            scores[trait.value] = responses.mean()
        return pd.Series(scores)