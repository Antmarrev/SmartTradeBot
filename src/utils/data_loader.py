
import yfinance as yf
import pandas as pd
import os

def download_data(ticker, start, end, save_csv=True, path="data/"):
    """
    Descarga datos históricos de Yahoo Finance.

    Args:
        ticker (str): Símbolo bursátil (ej: 'SPY')
        start (str): Fecha de inicio en formato 'YYYY-MM-DD'
        end (str): Fecha de fin en formato 'YYYY-MM-DD'
        save_csv (bool): Si True, guarda el CSV en la carpeta data/
        path (str): Ruta donde guardar el archivo CSV

    Returns:
        pd.DataFrame: Datos descargados
    """
    try:
        data = yf.download(ticker, start=start, end=end)

        if data.empty:
            print(f"[⚠️] No se encontraron datos para {ticker}.")
            return pd.DataFrame()

        if save_csv:
            os.makedirs(path, exist_ok=True)
            filename = f"{ticker}_{start}_{end}.csv"
            full_path = os.path.join(path, filename)
            data.to_csv(full_path)
            print(f"[✅] Datos guardados en {full_path}")

        return data

    except Exception as e:
        print(f"[❌] Error al descargar datos de {ticker}: {e}")
        return pd.DataFrame()
