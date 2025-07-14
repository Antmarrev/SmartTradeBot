# SmartTradeBot - Bot de Trading Inteligente (TFM)

**Autor:** Antonio Martín  
**Proyecto:** Trabajo Fin de Máster (TFM) - Máster en Project Management  
**Versión inicial:** MVP 0.1

## 🚀 Descripción

**SmartTradeBot** es un bot de trading algorítmico modular con avisador de señales, backtesting y visualización mediante un dashboard en Streamlit.

### 🎯 Objetivo

Desarrollar un sistema de trading automatizado que:

- Genere señales de compra/venta basadas en estrategias cuantitativas.
- Permita backtesting con métricas clave.
- Ofrezca una interfaz interactiva y visual para probar estrategias.
- Incluya módulos escalables para ejecución automática y aprendizaje automático.

Este proyecto combina la aplicación de **Project Management (PMI)** con el desarrollo de un producto tecnológico real.

## ⚙️ Funcionalidades previstas

- Estrategia base A1 (cruce de medias, RSI, etc.)
- Backtesting de estrategias
- Generador de señales (alertas por consola, log y futuros canales como Telegram/email)
- Dashboard interactivo en Streamlit
- Modularidad para añadir ejecución con broker y optimización con ML

## 🗂️ Estructura del proyecto

SmartTradeBot/
├── data/
├── notebooks/
├── src/
│ ├── strategies/
│ ├── backtesting/
│ ├── alerts/
│ ├── execution/
│ ├── optimization/
│ └── utils/
├── dashboard/
│ └── app.py
├── tests/
├── docs/
│ └── tfm/
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE

yaml
Copiar
Editar

## 📝 Licencia

MIT License

---

**Este proyecto está en desarrollo.**  
Primera versión funcional estimada: Agosto 2025.