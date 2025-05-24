from abc import ABC
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, validate_call


class FileParser(BaseModel, ABC):
    """Abstract base class for file parsers.

    Provides methods for checking file extensions and existence.
    """

    @validate_call
    def check_extension(self, path: Path, extension: str) -> None:
        """Check if the file has the expected extension."""
        if not path.suffix == extension:
            raise ValueError(f"Invalid file type: {path.suffix}. Expected {extension}")

    @validate_call
    def check_existence(self, path: Path) -> None:
        """Check if the file exists and is a file."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

    def check_file(self, path: Path, extension: str) -> None:
        """Check if the file exists and has the expected extension."""
        self.check_existence(path)
        self.check_extension(path, extension)

    def check_empty(self, df: pd.DataFrame) -> None:
        """Check if the DataFrame is empty."""
        if df.empty:
            raise ValueError("No data found in the file")
