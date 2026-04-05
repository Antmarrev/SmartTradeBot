"""
utils/data_loader.py — historical price data retrieval.
"""

import logging

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


def download_prices(
    tickers: list[str],
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Download daily adjusted closing prices for a list of tickers.

    Uses yfinance with auto_adjust=True, which returns adjusted prices
    under the standard 'Close' column.

    Args:
        tickers:    List of ticker symbols (e.g. ["SPY", "QQQ"]).
                    Values are stripped, uppercased, and deduplicated before use.
        start_date: Start date in "YYYY-MM-DD" format (inclusive).
        end_date:   End date in "YYYY-MM-DD" format. Coverage up to this date
                    depends on yfinance availability.

    Returns:
        DataFrame with a DatetimeIndex, one column per ticker, containing
        adjusted closing prices. Rows and columns that are entirely NaN
        are dropped.

    Raises:
        ValueError: If tickers is empty or dates are malformed.
        RuntimeError: If no data could be retrieved for any ticker.
    """
    # Normalize tickers
    cleaned = [t.strip().upper() for t in tickers if t.strip()]
    if not cleaned:
        raise ValueError("tickers must not be empty.")

    try:
        pd.Timestamp(start_date)
        pd.Timestamp(end_date)
    except Exception as exc:
        raise ValueError(f"Invalid date format: {exc}") from exc

    if pd.Timestamp(start_date) >= pd.Timestamp(end_date):
        raise ValueError(f"start_date ({start_date}) must be before end_date ({end_date}).")

    logger.info("Downloading data for %s from %s to %s", cleaned, start_date, end_date)

    raw: pd.DataFrame = yf.download(
        tickers=cleaned,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if raw.empty:
        raise RuntimeError(
            f"No data returned for tickers {cleaned} between {start_date} and {end_date}."
        )

    # yfinance returns a MultiIndex when multiple tickers are requested;
    # with a single ticker it returns a flat DataFrame.
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            prices = raw["Close"]
        else:
            raise RuntimeError("Expected 'Close' column not found in downloaded data.")
    else:
        # Single ticker — flat column names
        if "Close" in raw.columns:
            prices = raw[["Close"]].rename(columns={"Close": cleaned[0]})
        else:
            raise RuntimeError("Expected 'Close' column not found in downloaded data.")

    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "Date"

    # Drop columns and rows that are entirely NaN
    prices = prices.dropna(axis=1, how="all").dropna(axis=0, how="all")

    missing = [t for t in cleaned if t not in prices.columns]
    if missing:
        logger.warning("No data retrieved for tickers: %s — they were dropped.", missing)

    if prices.empty:
        raise RuntimeError("All tickers returned empty data after cleaning.")

    logger.info(
        "Downloaded %d rows x %d tickers (%s to %s).",
        len(prices),
        len(prices.columns),
        prices.index[0].date(),
        prices.index[-1].date(),
    )

    return prices
