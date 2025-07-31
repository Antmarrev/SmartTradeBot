from src.utils.data_loader import download_data
from src.strategies.cruce_medias import cruce_medias
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 1. Parámetros
    ticker = "SPY"
    start = "2020-01-01"
    end = "2025-07-28"

    # 2. Descargar datos
    df = download_data(ticker, start, end, save_csv=False)

    # 3. Aplicar estrategia
    df = cruce_medias(df, short_window=10, long_window=50)

    # 4. Crear gráfico
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label='Precio', color='black', alpha=0.6)
    plt.plot(df.index, df['short_ma'], label='Media Corta (10)', color='blue')
    plt.plot(df.index, df['long_ma'], label='Media Larga (50)', color='red')

    # 5. Señales
    buy_signals = df[df['signal'] == 1]
    sell_signals = df[df['signal'] == -1]

    plt.scatter(buy_signals.index, buy_signals['Close'], label='Compra', marker='^', color='green', s=100)
    plt.scatter(sell_signals.index, sell_signals['Close'], label='Venta', marker='v', color='red', s=100)

    plt.title(f"Estrategia de Cruce de Medias – {ticker}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
