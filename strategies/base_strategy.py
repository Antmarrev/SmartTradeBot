"""
strategies/base_strategy.py — abstract base interface for all strategies.
"""

from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    """Abstract base class for all trading strategies.

    Subclasses must implement:
        - name (property)
        - generate_signals(prices)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique, human-readable identifier for the strategy."""

    @abstractmethod
    def generate_signals(
        self, prices: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Compute entry and exit signals from price data.

        Args:
            prices: DataFrame of adjusted closing prices with a DatetimeIndex
                    and one column per ticker.

        Returns:
            A tuple (entries, exits) where both are boolean DataFrames with
            the same shape and index as prices.
            True marks the bar where the signal is triggered.
        """
