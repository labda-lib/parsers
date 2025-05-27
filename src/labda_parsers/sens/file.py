from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from ..parser import FileParser

SENS_NORMALIZATION_FACTOR = -4 / 512
DTYPE = np.dtype([("timestamp", "6uint8"), ("x", ">i2"), ("y", ">i2"), ("z", ">i2")])


class Sens(FileParser):
    """Parses for Sens binary files."""

    normalize: bool = True

    def _read(
        self,
        obj: Path | bytes,
        func: Callable,
    ) -> pd.DataFrame:
        data = func(obj, dtype=DTYPE, count=-1, offset=0)
        timestamps = np.dot(
            data["timestamp"], [1 << 40, 1 << 32, 1 << 24, 1 << 16, 1 << 8, 1]
        )

        df = pd.DataFrame(
            {
                "datetime": pd.to_datetime(timestamps, unit="ms", utc=True),
                "acc_x": data["x"].astype(np.int16),
                "acc_y": data["y"].astype(np.int16),
                "acc_z": data["z"].astype(np.int16),
            }
        )

        self.check_empty(df)

        df.set_index("datetime", inplace=True)

        if self.normalize:
            df = df * SENS_NORMALIZATION_FACTOR

        return df.astype(np.float32)

    def from_file(self, path: str | Path) -> pd.DataFrame:
        if isinstance(path, str):
            path = Path(path)

        self.check_file(path, ".bin")

        return self._read(path, np.fromfile)

    def from_buffer(self, buffer: bytes) -> pd.DataFrame:
        if not isinstance(buffer, bytes):
            raise TypeError("Expected a bytes object.")

        return self._read(buffer, np.frombuffer)
