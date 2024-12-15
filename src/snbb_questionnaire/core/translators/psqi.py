from enum import Enum
import warnings
from snbb_questionnaire.core.sheet_loader import SheetLoader
import pandas as pd
from datetime import datetime
import numpy as np


def date_to_time(timestamp: str) -> str:
    """
    Convert a date string to a time string.

    Parameters
    ----------
    timestamp : str
        The date string to convert.

    Returns
    -------
    str
        The time string.
    """
    try:
        return pd.to_datetime(timestamp).strftime("%H:%M:%S")
    except ValueError:
        return np.nan


def str_to_float(value: str) -> int:
    """
    Convert a string to an integer.

    Parameters
    ----------
    value : str
        The string to convert.

    Returns
    -------
    int
        The integer value of the string
    """
    try:
        return float(value)
    except ValueError:
        return np.nan


def replace_values(value: str, replace_dict: dict):
    """
    Replace values in a string using a dictionary.

    Parameters
    ----------
    value : str
        The string to replace values in.
    replace_dict : dict
        A dictionary of values to replace.

    Returns
    -------
    str
        The string with values replaced.
    """
    return replace_dict.get(value)


VALUES_DICT_1 = {
    "לא במהלך החודש האחרון": 0,
    "פחות מפעם בשבוע": 1,
    "פעם או פעמיים בשבוע": 2,
    "שלוש פעמים או יותר בשבוע": 3,
}

VALUES_DICT_2 = {"טובה מאוד": 0, "די טובה": 1, "די גרועה": 2, "גרועה מאוד": 3}

VALUES_DICT_3 = {
    "אין לי בן זוג או שותף לדירה": "no_partner",
    "בן זוג / שותף לדירה בחדר אחר": "partner_in_another_room",
    "בן זוג באותו חדר, אבל לא באותה מיטה": "partner_in_same_room_not_same_bed",
    "בן זוג באותה מיטה": "partner_in_same_bed",
}

VALUES_DICT_4 = {
    "לא התקשיתי כלל": 0,
    "התקשיתי מעט מאוד": 1,
    "די התקשיתי": 2,
    "התקשיתי מאוד": 3,
}

REPLACE_DICT = {
    "HW-PQSI001": {"func": date_to_time, "args": {}},
    "HW-PQSI002": {"func": str_to_float, "args": {}},
    "HW-PQSI003": {"func": date_to_time, "args": {}},
    "HW-PQSI004": {"func": str_to_float, "args": {}},
    "HW-PQSI005": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI006": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI007": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI008": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI009": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI010": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI011": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI012": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI013": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI014": None,
    "HW-PQSI015": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI016": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_2}},
    "HW-PQSI017": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI018": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI019": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_4}},
    "HW-PQSI020": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_3}},
    "HW-PQSI021": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI022": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI023": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI024": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
    "HW-PQSI025": None,
    "HW-PQSI026": {"func": replace_values, "args": {"replace_dict": VALUES_DICT_1}},
}


class PsqiQuestions(Enum):
    PQSI001 = "1"
    PQSI002 = "2"
    PQSI003 = "3"
    PQSI004 = "4"
    PQSI005 = "5a"
    PQSI006 = "5b"
    PQSI007 = "5c"
    PQSI008 = "5d"
    PQSI009 = "5e"
    PQSI010 = "5f"
    PQSI011 = "5g"
    PQSI012 = "5h"
    PQSI013 = "5i"
    PQSI014 = "5j_descriptive"
    PQSI015 = "5j"
    PQSI016 = "6"
    PQSI017 = "7"
    PQSI018 = "8"
    PQSI019 = "9"
    PQSI020 = "10"
    PQSI021 = "10a"
    PQSI022 = "10b"
    PQSI023 = "10c"
    PQSI024 = "10d"
    PQSI025 = "10e_descriptive"
    PQSI026 = "10e"


class PSQI:
    MANDATORY_QUESTIONS = [
        "1",
        "2",
        "3",
        "4",
        "5a",
        "5b",
        "5c",
        "5d",
        "5e",
        "5f",
        "5g",
        "5h",
        "5i",
        "5j",
        "6",
        "7",
        "8",
        "9",
    ]

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def _collect_psqi_questionnaire(self) -> pd.DataFrame:
        """
        Collect the PSQI questionnaire data.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the PSQI questionnaire data.
        """
        result = self.data[REPLACE_DICT.keys()]
        for column, func in REPLACE_DICT.items():
            if func:
                result[column] = result[column].apply(func["func"], **func["args"])
        return result.rename(
            columns={f"HW-{k.name}": k.value for k in PsqiQuestions},
        ).replace({"": np.nan})

    @staticmethod
    def duration_of_sleep(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        # IF Q4 > 7, THEN set value to 0
        # IF Q4 < 7 and > 6, THEN set value to 1
        # IF Q4 < 6 and > 5, THEN set value to 2
        # IF Q4 < 5, THEN set value to 3
        q4 = row["4"]
        if pd.isna(q4):
            return np.nan
        elif q4 > 7:
            result = 0
        elif q4 > 6:
            result = 1
        elif q4 > 5:
            result = 2
        else:
            result = 3
        return result

    @staticmethod
    def sleep_disturbance(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        # set the score for Q5J to 0 if either the comment or the value was missing.
        q5j, q5j_descriptive = row["5j"], row["5j_descriptive"]
        if pd.isna(q5j) or pd.isna(q5j_descriptive):
            q5j = 0
        q5b, q5c, q5d, q5e, q5f, q5g, q5h, q5i = (
            row["5b"],
            row["5c"],
            row["5d"],
            row["5e"],
            row["5f"],
            row["5g"],
            row["5h"],
            row["5i"],
        )
        if any(pd.isna(x) for x in [q5b, q5c, q5d, q5e, q5f, q5g, q5h, q5i]):
            return np.nan
        # IF Q5b + Q5c + Q5d + Q5e + Q5f + Q5g + Q5h + Q5i + Q5j = 0, THEN set value to 0
        # IF Q5b + Q5c + Q5d + Q5e + Q5f + Q5g + Q5h + Q5i + Q5j >= 1 and <= 9, THEN set value to 1
        # IF Q5b + Q5c + Q5d + Q5e + Q5f + Q5g + Q5h + Q5i + Q5j > 9 and <= 18, THEN set value to 2
        # IF Q5b + Q5c + Q5d + Q5e + Q5f + Q5g + Q5h + Q5i + Q5j > 18, THEN set value to 3
        result = q5b + q5c + q5d + q5e + q5f + q5g + q5h + q5i + q5j
        if 1 <= result <= 9:
            result = 1
        elif 9 < result <= 18:
            result = 2
        elif result > 18:
            result = 3
        return result

    @staticmethod
    def sleep_latency(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        # First, recode Q2 into Q2new thusly:
        # IF Q2 > 0 and < 15, THEN set value of Q2new to 0
        # IF Q2 > 15 and < 30, THEN set value of Q2new to 1
        # IF Q2 > 30 and < 60, THEN set value of Q2new to 2
        # IF Q2 > 60, THEN set value of Q2new to 3
        q2 = row["2"]
        if pd.isna(q2):
            return np.nan
        elif 0 < q2 < 15:
            q2new = 0
        elif 15 < q2 < 30:
            q2new = 1
        elif 30 < q2 < 60:
            q2new = 2
        else:
            q2new = 3
        # Next
        # IF Q5a + Q2new = 0, THEN set value to 0
        # IF Q5a + Q2new > 1 and < 2, THEN set value to 1
        # IF Q5a + Q2new > 3 and < 4, THEN set value to 2
        # IF Q5a + Q2new > 5 and < 6, THEN set value to 3
        q5a = row["5a"]
        if pd.isna(q5a):
            return np.nan
        result = q5a + q2new
        if result == 0:
            result = 0
        elif 1 < result < 2:
            result = 1
        elif 3 < result < 4:
            result = 2
        elif 5 < result < 6:
            result = 3
        return result

    @staticmethod
    def sleep_dysfunction(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        # IF Q8 + Q9 = 0, THEN set value to 0
        # IF Q8 + Q9 > 1 and < 2, THEN set value to 1
        # IF Q8 + Q9 > 3 and < 4, THEN set value to 2
        # IF Q8 + Q9 > 5 and < 6, THEN set value to 3
        q8, q9 = row["8"], row["9"]
        if any(pd.isna(x) for x in [q8, q9]):
            return np.nan
        result = q8 + q9
        if result == 0:
            result = 0
        elif 1 < result < 2:
            result = 1
        elif 3 < result < 4:
            result = 2
        elif 5 < result < 6:
            result = 3
        return result

    @staticmethod
    def sleep_efficiency(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        # Diffsec = Diffsec = Difference in seconds between times for Bed Time (Q1) and
        # Getting Up Time (Q3).
        # Diffhour = Absolute value of diffsec / 3600
        # newtib =IF diffhour > 24, then newtib = diffhour – 24
        # IF diffhour < 24, THEN newtib = diffhour
        # (NOTE, THE ABOVE JUST CALCULATES THE HOURS BETWEEN BED
        # TIME (Q1) AND GETTING UP TIME (Q3)
        # tmphse = (Q4 / newtib) * 100
        # row 3 and row 1 are the bed time and getting up time respectively, so
        # calculate time difference accordingly (they're strings)

        q1 = row["1"]
        q3 = row["3"]
        q4 = row["4"]
        if any(pd.isna(x) for x in [q1, q3, q4]):
            return np.nan
        diffsec = (
            datetime.strptime(q3, "%H:%M:%S") - datetime.strptime(q1, "%H:%M:%S")
        ).total_seconds()
        diffhour = abs(diffsec) / 3600
        newtib = diffhour - 24 if diffhour > 24 else diffhour
        tmphse = (q4 / newtib) * 100

        # IF tmphse > 85, THEN set value to 0
        # IF tmphse < 85 and > 75, THEN set value to 1
        # IF tmphse < 75 and > 65, THEN set value to 2
        # IF tmphse < 65, THEN set value to 3
        if tmphse > 85:
            result = 0
        elif 75 < tmphse < 85:
            result = 1
        elif 65 < tmphse < 75:
            result = 2
        else:
            result = 3
        return result

    @staticmethod
    def sleep_quality(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        return row["6"]

    @staticmethod
    def need_meds_to_sleep(row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        return row["7"]

    def psqi_score(self, row: pd.Series) -> int:
        """
        Convert values in the PSQI DataFrame.

        Parameters
        ----------
        psqi_df : pd.DataFrame
            The PSQI DataFrame to convert.
        """
        # IF Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9 + Q10 = 0, THEN set value to 0
        # IF Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9 + Q10 > 1 and < 10, THEN set value to 1
        # IF Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9 + Q10 > 11 and < 20, THEN set value to 2
        # IF Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9 + Q10 > 21, THEN set value to 3
        result = {}
        for key, func in zip(
            [
                "duration",
                "disturbance",
                "latency",
                "dysfunction",
                "efficiency",
                "quality",
                "meds",
            ],
            [
                self.duration_of_sleep,
                self.sleep_disturbance,
                self.sleep_latency,
                self.sleep_dysfunction,
                self.sleep_efficiency,
                self.sleep_quality,
                self.need_meds_to_sleep,
            ],
        ):
            try:
                result[key] = func(row)
            except Exception as e:
                warnings.warn(f"Error in calculating PSQI score: {e}")
                result[key] = np.nan
        result["psqi_score"] = np.sum(list(result.values()))
        return result
