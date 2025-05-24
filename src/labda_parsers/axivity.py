from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from skdh.io import ReadCwa

from .parser import FileParser


class Axivity(FileParser):
    """Parser for Axivity files.

    Attributes:
        timezone (ZoneInfo | None): Timezone to localize the datetime index to.
    """

    timezone: ZoneInfo | None = None

    def from_cwa(
        self,
        path: Path | str,
    ) -> pd.DataFrame:
        self.check_file(path, ".cwa")

        cwa = ReadCwa().predict(file=path, tz_name=self.timezone)
        cwa["time"] = np.array(cwa["time"], dtype="datetime64[s]")

        df = pd.DataFrame(
            cwa["accel"].astype(np.float32),
            columns=["acc_x", "acc_y", "acc_z"],
            index=cwa["time"],
        )

        df.index.name = "datetime"
        if self.timezone:
            df.index = pd.to_datetime(df.index, utc=True)
            df.index = df.index.tz_convert("Europe/Copenhagen")
        else:
            df.index = pd.to_datetime(df.index)

        temperature = cwa.get("temperature")

        if temperature is not None:
            df["temperature"] = temperature.astype(np.float32)

        self.check_empty(df)

        return df
