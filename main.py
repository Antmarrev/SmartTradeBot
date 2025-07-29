from src.utils.data_loader import download_data

if __name__ == "__main__":
    ticker = "SPY"
    start = "2020-01-01"
    end = "2025-07-28"

    data = download_data(ticker, start, end)

    print("\n📊 Últimos datos descargados:")
    print(data.tail())
