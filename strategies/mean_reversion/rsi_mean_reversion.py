"""
strategies/mean_reversion/rsi_mean_reversion.py — RSI-based mean reversion strategy.
"""

import pandas as pd

from strategies.base_strategy import BaseStrategy


def _compute_rsi(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """Compute RSI for each column using Wilder's smoothing (EWM).

    Args:
        prices: DataFrame of closing prices.
        window: Lookback period.

    Returns:
        DataFrame of RSI values with the same shape as prices.
    """
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


class RSIMeanReversionStrategy(BaseStrategy):
    """Mean reversion strategy driven by the Relative Strength Index (RSI).

    Generates signals on threshold crossings:
    - Entry: RSI crosses below entry_threshold (previous >= threshold, current < threshold).
    - Exit:  RSI crosses above exit_threshold  (previous <= threshold, current > threshold).

    Args:
        rsi_window:        Lookback period for RSI calculation. Default: 14.
        entry_threshold:   RSI level crossed below to trigger a long entry. Default: 30.
        exit_threshold:    RSI level crossed above to trigger an exit. Default: 50.
    """

    def __init__(
        self,
        rsi_window: int = 14,
        entry_threshold: float = 30.0,
        exit_threshold: float = 50.0,
    ) -> None:
        if rsi_window < 2:
            raise ValueError(f"rsi_window must be >= 2, got {rsi_window}.")
        if not (0 < entry_threshold < exit_threshold < 100):
            raise ValueError(
                f"Thresholds must satisfy 0 < entry ({entry_threshold}) "
                f"< exit ({exit_threshold}) < 100."
            )
        self.rsi_window = rsi_window
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold

    @property
    def name(self) -> str:
        return (
            f"RSIMeanReversion(window={self.rsi_window}, "
            f"entry={self.entry_threshold}, exit={self.exit_threshold})"
        )

    def generate_signals(
        self, prices: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Generate entry and exit signals based on RSI threshold crossings.

        Args:
            prices: DataFrame of adjusted closing prices with a DatetimeIndex
                    and one column per ticker.

        Returns:
            A tuple (entries, exits) of boolean DataFrames with the same
            index and columns as prices.
            entries: True on the bar where RSI crosses below entry_threshold.
            exits:   True on the bar where RSI crosses above exit_threshold.
        """
        if prices.empty:
            raise ValueError("prices DataFrame must not be empty.")

        rsi = _compute_rsi(prices, self.rsi_window)
        rsi_prev = rsi.shift(1)

        entries = (
            (rsi_prev >= self.entry_threshold) & (rsi < self.entry_threshold)
        ).fillna(False).astype(bool)

        exits = (
            (rsi_prev <= self.exit_threshold) & (rsi > self.exit_threshold)
        ).fillna(False).astype(bool)

        return entries, exits
