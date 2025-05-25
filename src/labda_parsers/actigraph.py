import io
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd
from pygt3x.reader import FileReader

from .parser import FileParser


@dataclass
class Actigraph(FileParser):
    """Parser for Actigraph files.

    Attributes:
        idle_sleep (IdleSleep): How to handle idle sleep mode.
            "ffill" will forward fill the last valid value.
            "zero" will set the accelerometer values to 0 during idle sleep.
            Defaults to "ffill".
    """

    idle_sleep: Literal["ffill", "zero"] = "ffill"

    def __post_init__(self):
        if self.idle_sleep not in {"ffill", "zero"}:
            raise ValueError(
                f"Invalid idle_sleep value: {self.idle_sleep}. Expected 'ffill' or 'zero'."
            )

    def from_file(
        self,
        path: Path | str,
    ) -> pd.DataFrame:
        if isinstance(path, str):
            path = Path(path)

        self.check_file(path, ".gt3x")

        with (
            FileReader(path) as reader,
            redirect_stdout(io.StringIO()),
        ):
            df = reader.to_pandas()
            timezone = reader.info.timezone

        self.check_empty(df)

        df.rename(
            columns={"X": "acc_x", "Y": "acc_y", "Z": "acc_z", "IdleSleepMode": "idle"},
            inplace=True,
        )
        df.index.name = "datetime"
        df.index = pd.to_datetime(df.index, unit="s")

        if timezone:
            df.index = df.index.tz_localize(timezone)

        if self.idle_sleep == "zero":
            df.loc[df["idle"], ["acc_x", "acc_y", "acc_z"]] = 0

        df.drop(columns="idle", inplace=True)

        return df
