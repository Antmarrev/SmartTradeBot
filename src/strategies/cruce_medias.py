import pandas as pd

def cruce_medias(df, short_window=10, long_window=50):
    """
    Estrategia de cruce de medias móviles simples.

    Args:
        df (pd.DataFrame): Datos con columnas de precios (debe tener 'Close')
        short_window (int): Periodos para la media móvil corta
        long_window (int): Periodos para la media móvil larga

    Returns:
        pd.DataFrame: Mismo DataFrame con columnas 'short_ma', 'long_ma' y 'signal'
    """
    df = df.copy()

    df['short_ma'] = df['Close'].rolling(window=short_window).mean()
    df['long_ma'] = df['Close'].rolling(window=long_window).mean()

    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1

    return df