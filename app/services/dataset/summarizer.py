"""..."""

import pandas as pd


class DatasetSummarizer:
    """..."""

    @staticmethod
    def summarize(df: pd.DataFrame, name: str) -> str:
        """..."""
        rows, columns = df.shape
        columns_summary = "\n".join(f"* {col} ({df[col].dtype})" for col in df.columns)
        return f"Dataset '{name}' has {rows} rows and {columns} columns:\n{columns_summary}"
