"""
SmartTraderBot — entry point.

Usage:
    python main.py
    python main.py --config config/settings.yaml
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config(path: str) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if config is None:
        raise ValueError(f"Config file is empty: {config_path}")
    if not isinstance(config, dict):
        raise ValueError(f"Config file must be a YAML mapping, got {type(config).__name__}")
    return config


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(config: dict[str, Any]) -> None:
    log_cfg = config.get("logging", {})

    level = getattr(logging, log_cfg.get("level", "INFO").upper(), logging.INFO)
    fmt = log_cfg.get("format", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    datefmt = log_cfg.get("date_format", "%Y-%m-%d %H:%M:%S")

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    if log_cfg.get("log_to_file", False):
        log_file = Path(log_cfg["log_file"])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=level, format=fmt, datefmt=datefmt, handlers=handlers, force=True)


# ---------------------------------------------------------------------------
# System bootstrap
# ---------------------------------------------------------------------------

def bootstrap(config: dict[str, Any]) -> None:
    logger = logging.getLogger(__name__)

    market = config["market"]
    backtest = config["backtest"]
    costs = config["costs"]

    logger.info("SmartTraderBot initialising")
    logger.info(
        "Universe: %s | Timeframe: %s | Tickers: %s",
        market["universe"],
        market["timeframe"],
        ", ".join(market["default_tickers"]),
    )
    logger.info(
        "Backtest window: %s → %s | Capital: $%s",
        backtest["start_date"],
        backtest["end_date"],
        f"{backtest['initial_capital']:,}",
    )
    logger.info(
        "Costs — commission: %.3f%% | slippage: %.3f%%",
        costs["commission"] * 100,
        costs["slippage"] * 100,
    )
    logger.info("System ready — plug in a strategy and run.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SmartTraderBot")
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Path to the YAML configuration file (default: config/settings.yaml)",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    args = parse_args()
    try:
        config = load_config(args.config)
        setup_logging(config)
        bootstrap(config)
    except Exception:
        logging.getLogger(__name__).exception("Startup failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
