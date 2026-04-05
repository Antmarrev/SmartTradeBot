# SmartTraderBot

A modular Python system for building and validating quantitative trading strategies through a structured research process.

SmartTraderBot is not a trading bot in the traditional sense. It is a research platform designed to systematically develop, test, and validate quantitative trading strategies. The goal is to build a rigorous pipeline — from raw market data to evidence-based strategy evaluation — rather than to produce signals for live trading.

---

## Vision

The long-term objective is to build a system of agents capable of:

- consuming financial literature and established quantitative principles
- generating strategy hypotheses grounded in economic or statistical reasoning
- validating those hypotheses through backtesting, out-of-sample testing, and robustness checks

Ultimately, the system is intended to evolve into an agent-based research pipeline where parts of the process — idea generation, formalisation, and empirical validation — can be progressively automated. Transparency and human control remain central: every decision made by the system should be inspectable and overridable.

The system is intended to operate as a research assistant rather than a black box: every strategy should be traceable to a clear rationale, and every result should be reproducible.

---

## Current Scope (V1)

This is an early-stage foundation. What is implemented so far:

- **Project structure** — clean, modular layout separating concerns across data, strategies, backtesting, and configuration
- **Data ingestion** — downloads adjusted daily price data for multiple tickers via `yfinance`
- **Strategy interface** — abstract base class defining a consistent contract for all strategies
- **First strategy** — RSI Mean Reversion: enters on RSI crossing below an oversold threshold and exits on recovery above a neutral level
- **Configuration** — YAML-based settings for market universe, costs, and performance thresholds
- **Logging** — structured logging throughout the pipeline

---

## Project Structure

```
SmartTraderBot/
├── config/
│   └── settings.yaml          # Market universe, costs, metrics thresholds, logging
├── utils/
│   └── data_loader.py         # Price data download and cleaning
├── strategies/
│   ├── base_strategy.py       # Abstract base class for all strategies
│   └── mean_reversion/
│       └── rsi_mean_reversion.py
├── backtesting/               # Backtest runner and metrics (in progress)
└── main.py                    # Entry point: loads config, initialises logging
```

---

## Example Workflow

At a high level, the system follows a simple and explicit pipeline:

```
# Data → Signals → Backtest → Evaluation
prices = download_prices(tickers, start_date, end_date)
    |
    v
strategy = RSIMeanReversionStrategy(rsi_window=14, entry_threshold=30, exit_threshold=50)
entries, exits = strategy.generate_signals(prices)
    |
    v
portfolio = run_backtest(prices, entries, exits, commission, slippage, initial_capital)
    |
    v
metrics = evaluate(portfolio)   # Sharpe, drawdown, profit factor, win rate, ...
```

Each layer is independent. Strategies produce signals; the backtesting layer consumes them. Neither knows about the other's internals.

---

## Getting Started

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the entry point:**

```bash
python main.py
```

By default, this loads `config/settings.yaml`, initialises logging, and confirms the system is ready. Strategy execution and backtesting will be wired into `main.py` as those layers are completed.

**Override config path:**

```bash
python main.py --config path/to/custom_settings.yaml
```

---

## Roadmap

- [ ] Backtest runner and metrics evaluation (vectorbt integration)
- [ ] Additional strategies: momentum, trend-following, volatility-based
- [ ] Robustness checks: walk-forward analysis, parameter sensitivity
- [ ] Portfolio layer: multi-asset allocation and position sizing
- [ ] Agent-based framework: hypothesis generation from quant literature
- [ ] Reporting: structured output of results per strategy run

---

## Philosophy

A few principles that guide this project:

**Evidence over intuition.** Every strategy must be grounded in a clear hypothesis — statistical, economic, or structural. Strategies that only fit historical data are not useful.

**No overfitting.** Parameter choices are constrained and validated out-of-sample. Performance thresholds in `settings.yaml` exist to filter out results that only look good on the training window.

**Reproducibility.** Given the same data and configuration, the system must produce the same results. No hidden state, no randomness without explicit seeds.

**Modularity.** Each component — data, signals, backtesting, evaluation — is replaceable. The system should be easy to extend without rewriting existing parts.

The goal is not to find strategies that simply appear to work. The goal is to build a system that can reliably reject the ones that do not.

The project is intentionally built incrementally, with each layer validated before increasing complexity.

---

## Disclaimer

This project is for research and educational purposes only. It does not constitute financial or investment advice. Nothing in this repository should be interpreted as a recommendation to buy or sell any financial instrument.

---

## License

MIT
