from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from skdh.io import ReadCwa

from .parser import FileParser


class Axivity(FileParser):
    """Parser for Axivity file.

    Attributes:
        timezone (ZoneInfo | None): Timezone to localize the datetime index to.
    """

    timezone: ZoneInfo | None = None

    def from_file(
        self,
        path: Path | str,
    ) -> pd.DataFrame:
        if isinstance(path, str):
            path = Path(path)

        self.check_file(path, ".cwa")

        cwa = ReadCwa().predict(file=path, tz_name=self.timezone)
        df = pd.DataFrame(
            cwa["accel"].astype(np.float32),
            columns=["acc_x", "acc_y", "acc_z"],
            index=cwa["time"],
        )

        temperature = cwa.get("temperature")
        if temperature is not None:
            df["temperature"] = temperature.astype(np.float32)

        del cwa

        df.index.name = "datetime"
        if self.timezone:
            df.index = pd.to_datetime(df.index, utc=True, unit="s")
            df.index = df.index.tz_convert("Europe/Copenhagen")
        else:
            df.index = pd.to_datetime(df.index, unit="s")

        self.check_empty(df)

        return df
