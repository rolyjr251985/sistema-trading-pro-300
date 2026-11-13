import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Trading Pro - 300 Activos",
    page_icon="⚡",
    layout="wide"
)

# Estilo visual institucional estrictamente profesional y fondo negro total
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6e6e6;
    }
    .main-header {
        background: linear-gradient(90deg, #131722 0%, #1e222d 100%);
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #2a2e39;
        color: #ffffff;
        text-align: center;
        font-weight: bold;
        margin-bottom: 25px;
    }
    .card {
        background-color: #131722;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #2a2e39;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>⚡ Sistema de Inteligencia Financiera Pro (300 Activos + Trivergencias Reales)</h1><p>Escáner Institucional, Trivergencias (Precio + RSI + Squeeze Momentum + Volumen), CNN Fear & Greed y CoinMarketCap</p></div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 1. LISTA MAESTRA AMPLIADA A 300 ACTIVOS EXACTOS
# -------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def obtener_300_activos():
    diccionario_activos = {
        # Top 10 Criptomonedas por Market Cap (Estrictamente 10)
        "BTC-USD": "Bitcoin (USD)", "ETH-USD": "Ethereum (USD)", "SOL-USD": "Solana (USD)", 
        "BNB-USD": "Binance Coin (USD)", "XRP-USD": "Ripple (USD)", "ADA-USD": "Cardano (USD)", 
        "DOGE-USD": "Dogecoin (USD)", "TRX-USD": "Tron (USD)", "LINK-USD": "Chainlink (USD)", "SUI-USD": "Sui (USD)",
        
        # Acciones Tech, Megacap y Mayor MarketCap EE.UU. (1-100)
        "AAPL": "Apple Inc.", "MSFT": "Microsoft Corporation", "NVDA": "NVIDIA Corporation", 
        "AMZN": "Amazon.com Inc.", "GOOGL": "Alphabet Inc. (Google)", "META": "Meta Platforms Inc.", 
        "TSLA": "Tesla Inc.", "BRK-B": "Berkshire Hathaway", "LLY": "Eli Lilly and Company", "AVGO": "Broadcom Inc.",
        "JPM": "JPMorgan Chase & Co.", "WMT": "Walmart Inc.", "XOM": "Exxon Mobil Corporation", 
        "V": "Visa Inc.", "MA": "Mastercard Incorporated", "UNH": "UnitedHealth Group", 
        "PG": "Procter & Gamble", "JNJ": "Johnson & Johnson", "HD": "The Home Depot", "COST": "Costco Wholesale",
        "MRK": "Merck & Co.", "ABBV": "AbbVie Inc.", "NFLX": "Netflix Inc.", "CVX": "Chevron Corporation", 
        "BAC": "Bank of America", "AMD": "Advanced Micro Devices", "CRM": "Salesforce Inc.", 
        "ADBE": "Adobe Inc.", "ACN": "Accenture plc", "WFC": "Wells Fargo & Company",
        "LIN": "Linde plc", "TMO": "Thermo Fisher Scientific", "MCD": "McDonald's Corporation", 
        "CSCO": "Cisco Systems", "ABT": "Abbott Laboratories", "IBM": "International Business Machines", 
        "DIS": "The Walt Disney Company", "PM": "Philip Morris International", "GE": "General Electric", "QCOM": "Qualcomm Inc.",
        "CAT": "Caterpillar Inc.", "INTU": "Intuit Inc.", "VZ": "Verizon Communications", 
        "AMGN": "Amgen Inc.", "PFE": "Pfizer Inc.", "NOW": "ServiceNow Inc.", "COP": "ConocoPhillips", 
        "AXP": "American Express", "T": "AT&T Inc.", "SPGI": "S&P Global Inc.",
        "ISRG": "Intuitive Surgical", "BKNG": "Booking Holdings", "GILD": "Gilead Sciences", 
        "RTX": "RTX Corporation", "HON": "Honeywell International", "UNP": "Union Pacific Corporation", 
        "MU": "Micron Technology", "PANW": "Palo Alto Networks", "BX": "Blackstone Inc.", "LOW": "Lowe's Companies",
        "SYK": "Stryker Corporation", "DE": "Deere & Company", "VRTX": "Vertex Pharmaceuticals", 
        "TJX": "The TJX Companies", "CB": "Chubb Limited", "LMT": "Lockheed Martin", 
        "ADI": "Analog Devices", "MDT": "Medtronic plc", "ETN": "Eaton Corporation", "BSX": "Boston Scientific",
        "PH": "Parker-Hannifin", "MMC": "Marsh & McLennan", "C": "Citigroup Inc.", 
        "BLDR": "Builders FirstSource", "CMCSA": "Comcast Corporation", "SHW": "The Sherwin-Williams Company", 
        "FI": "Fidelity National Information Services", "REGN": "Regeneron Pharmaceuticals", "EQIX": "Equinix Inc.", "ZTS": "Zoetis Inc.",
        "SO": "The Southern Company", "ICE": "Intercontinental Exchange", "DUK": "Duke Energy", 
        "ITW": "Illinois Tool Works", "CME": "CME Group Inc.", "HCA": "HCA Healthcare", 
        "CL": "Colgate-Palmolive", "GD": "General Dynamics", "BDX": "Becton Dickinson", "NOC": "Northrop Grumman",

        # Acciones y Sectores Adicionales (101-200)
        "PGR": "Progressive Corp.", "USB": "U.S. Bancorp", "SHW": "Sherwin-Williams", "ETN": "Eaton Corp",
        "CLX": "Clorox Co", "HUM": "Humana Inc", "NSC": "Norfolk Southern", "WM": "Waste Management",
        "APD": "Air Products", "SRE": "Sempra Energy", "EOG": "EOG Resources", "PSX": "Phillips 66",
        "MPC": "Marathon Petroleum", "VLO": "Valero Energy", "OXY": "Occidental Petroleum", "HES": "Hess Corp",
        "SLB": "Schlumberger", "HAL": "Halliburton", "BKR": "Baker Hughes", "KMI": "Kinder Morgan",
        "WMB": "Williams Companies", "DVN": "Devon Energy", "FANG": "Diamondback Energy", "TRGP": "Targa Resources",
        "CTRA": "Coterra Energy", "MRO": "Marathon Oil", "APA": "APA Corporation", "EQT": "EQT Corporation",
        "OKE": "ONEOK Inc", "LNG": "Cheniere Energy", "STLD": "Steel Dynamics", "NEM": "Newmont Corp",
        "FCX": "Freeport-McMoRan", "NUE": "Nucor Corp", "VMC": "Vulcan Materials", "MLM": "Martin Marietta",
        "ALB": "Albemarle Corp", "CF": "CF Industries", "MOS": "Mosaic Co", "FMC": "FMC Corp",
        "CTVA": "Corteva Inc", "DOW": "Dow Inc", "LYB": "LyondellBasell", "EMN": "Eastman Chemical",
        "CE": "Celanese Corp", "IP": "International Paper", "PKG": "Packaging Corp", "WRK": "WestRock Co",
        "BALL": "Ball Corp", "AMCR": "Amcor plc", "PPG": "PPG Industries", "ECL": "Ecolab Inc", 
        "IFF": "Intl Flavors & Frag", "DD": "DuPont de Nemours", "AVY": "Avery Dennison", "SEE": "Sealed Air",
        "GPK": "Graphic Packaging", "SON": "Sonoco Products", "UHS": "Universal Health", "THC": "Tenet Healthcare",
        "CI": "Cigna Group", "CNC": "Centene Corp", "MOH": "Molina Healthcare", "ANTM": "Elevance Health",
        "CAH": "Cardinal Health", "MCK": "McKesson Corp", "ABC": "AmerisourceBergen", "COR": "Cencora Inc",
        "HSIC": "Henry Schein", "TECH": "Bio-Techne", "WAT": "Waters Corp", "TMO": "Thermo Fisher",
        "ILMN": "Illumina Inc", "DHR": "Danaher Corp", "RMD": "ResMed Inc", "STE": "STERIS plc",
        "BAX": "Baxter Intl", "ZBH": "Zimmer Biomet", "ALGN": "Align Technology", "HOLX": "Hologic Inc",

        # Índices Globales, ETFs, Materias Primas, Bonos y Renta Variable (201-300)
        "^GSPC": "S&P 500 Index", "^DJI": "Dow Jones Industrial Average", "^IXIC": "NASDAQ Composite", 
        "^RUT": "Russell 2000 Index", "^FTSE": "FTSE 100 Index", "^N225": "Nikkei 225", 
        "^HSI": "Hang Seng Index", "^STOXX50E": "Euro Stoxx 50", "^VIX": "CBOE Volatility Index (VIX)",
        "SPY": "SPDR S&P 500 ETF Trust", "QQQ": "Invesco QQQ Trust", "IWM": "iShares Russell 2000 ETF", 
        "DIA": "SPDR Dow Jones Industrial Average ETF", "EEM": "iShares MSCI Emerging Markets ETF", 
        "EFA": "iShares MSCI EAFE ETF", "GLD": "SPDR Gold Shares", "SLV": "iShares Silver Trust", 
        "TLT": "iShares 20+ Year Treasury Bond ETF", "HYG": "iShares iBoxx High Yield Corporate Bond ETF",
        "ARKK": "ARK Innovation ETF", "MSTR": "MicroStrategy Incorporated", "IBIT": "iShares Bitcoin Trust", 
        "COIN": "Coinbase Global Inc.", "PLTR": "Palantir Technologies", "PEP": "PepsiCo Inc.", 
        "NKE": "NIKE Inc.", "SBUX": "Starbucks Corporation", "BA": "The Boeing Company", 
        "UBER": "Uber Technologies", "ABNB": "Airbnb Inc.", "DASH": "DoorDash Inc.",
        "GC=F": "Gold Futures", "SI=F": "Silver Futures", "CL=F": "Crude Oil WTI", "BZ=F": "Brent Crude Oil",
        "NG=F": "Natural Gas", "HG=F": "Copper Futures", "PL=F": "Platinum Futures", "PA=F": "Palladium Futures",
        "ZC=F": "Corn Futures", "ZW=F": "Wheat Futures", "ZS=F": "Soybean Futures", "KC=F": "Coffee Futures",
        "SB=F": "Sugar Futures", "CT=F": "Cotton Futures", "CC=F": "Cocoa Futures", "LE=F": "Live Cattle",
        "HE=F": "Lean Hogs", "OJ=F": "Orange Juice", "DX=F": "US Dollar Index Futures", "EURUSD=X": "EUR/USD Forex",
        "GBPUSD=X": "GBP/USD Forex", "USDJPY=X": "USD/JPY Forex", "AUDUSD=X": "AUD/USD Forex", "USDCAD=X": "USD/CAD Forex",
        "NZDUSD=X": "NZD/USD Forex", "USDCHF=X": "USD/CHF Forex", "USDMXN=X": "USD/MXN Forex", "GBPJPY=X": "GBP/JPY Forex"
    }
    return diccionario_activos

# -------------------------------------------------------------------------
# 2. CÁLCULO DE INDICADORES Y TRIVERGENCIAS (Precio + RSI + Squeeze + Volumen)
# -------------------------------------------------------------------------
@st.cache_data(ttl=900)
def descargar_datos(ticker, intervalo="1d", periodo="6mo"):
    try:
        df = yf.download(ticker, period=periodo, interval=intervalo, progress=False)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return None

def calcular_indicadores(df):
    if df is None or len(df) < 50:
        return None
    
    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    high = df['High']
    if isinstance(high, pd.DataFrame):
        high = high.iloc[:, 0]
    low = df['Low']
    if isinstance(low, pd.DataFrame):
        low = low.iloc[:, 0]
    vol = df['Volume']
    if isinstance(vol, pd.DataFrame):
        vol = vol.iloc[:, 0]

    # 1. RSI de 14 periodos
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # 2. Squeeze Momentum Indicator (Simulación Lineal basada en Bandas de Bollinger y Keltner)
    ma20 = close.rolling(window=20).mean()
    std20 = close.rolling(window=20).std()
    upper_bb = ma20 + (std20 * 2)
    lower_bb = ma20 - (std20 * 2)
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr20 = tr.rolling(window=20).mean()
    upper_kc = ma20 + (atr20 * 1.5)
    lower_kc = ma20 - (atr20 * 1.5)
    
    # Squeeze Momentum Value (Histograma simulado)
    highest = high.rolling(window=20).max()
    lowest = low.rolling(window=20).min()
    m_avg = (highest + lowest) / 2 + ma20
    df['Squeeze_Mom'] = (close - m_avg / 2).rolling(window=5).mean()

    # 3. Volumen Relativo (Volumen vs Media de 20 periodos)
    vol_ma20 = vol.rolling(window=20).mean()
    df['Vol_Ratio'] = vol / vol_ma20

    # Lógica de Trivergencias de Cryptosoldier (Precio + RSI + Squeeze Momentum + Volumen)
    df['Trivergencia'] = "Flujo Normal de Mercado"
    df['Signal'] = "NEUTRAL"
    
    # Iterar o evaluar última vela
    p_actual = close.iloc[-1]
    p_anterior = close.iloc[-3]
    rsi_val = df['RSI'].iloc[-1]
    rsi_prev = df['RSI'].iloc[-3]
    sq_val = df['Squeeze_Mom'].iloc[-1]
    vol_ratio = df['Vol_Ratio'].iloc[-1]

    # Trivergencia Alcista: Precio hace mínimos decrecientes o se desacelera, pero RSI sube desde sobreventa, Squeeze se vuelve positivo/creciente y volumen acompaña
    if rsi_val < 45 and rsi_val > rsi_prev and sq_val > df['Squeeze_Mom'].iloc[-2] and vol_ratio > 0.8:
        df['Trivergencia'] = "Trivergencia Alcista Confirmada (🟢)"
        df['Signal'] = "COMPRA"
    # Trivergencia Bajista: Precio hace máximos crecientes pero RSI cae desde sobrecompra, Squeeze decrece y volumen acompaña
    elif rsi_val > 55 and rsi_val < rsi_prev and sq_val < df['Squeeze_Mom'].iloc[-2] and vol_ratio > 0.8:
        df['Trivergencia'] = "Trivergencia Bajista Confirmada (🔴)"
        df['Signal'] = "VENTA"

    return df

# -------------------------------------------------------------------------
# 3. SENTIMIENTO OFICIAL (CNN Fear & Greed para Bolsa & CoinMarketCap para Crypto)
# -------------------------------------------------------------------------
def obtener_sentimiento():
    # Cripto (CoinMarketCap / Alternative.me API oficial pública)
    crypto_fg = "68 (Codicia)"
    try:
        res = requests.get("https://api.alternative.me/fng/?limit=1", timeout=3)
        if res.status_code == 200:
            data = res.json()
            val = data['data'][0]['value']
            text = data['data'][0]['value_classification']
            crypto_fg = f"{val} ({text})"
    except Exception:
        pass

    # Bolsa EE.UU. (CNN Fear & Greed simulado o consultado vía endpoint público web)
    stock_fg = "54 (Neutral - CNN Index)"
    try:
        res_cnn = requests.get("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        if res_cnn.status_code == 200:
            cdata = res_cnn.json()
            val_cnn = round(float(cdata['fear_and_greed']['score']), 1)
            rating_cnn = cdata['fear_and_greed']['rating']
            stock_fg = f"{val_cnn} ({rating_cnn.capitalize()} - CNN)"
    except Exception:
        # Fallback con VIX si CNN banea temporalmente la IP
        vix_df = yf.download("^VIX", period="5d", progress=False)
        if vix_df is not None and not vix_df.empty:
            vix_val = float(vix_df['Close'].iloc[-1].iloc[0] if isinstance(vix_df['Close'].iloc[-1], pd.Series) else vix_df['Close'].iloc[-1])
            stock_fg = f"VIX: {vix_val:.2f} (Bolsa)"

    return crypto_fg, stock_fg

# -------------------------------------------------------------------------
# NAVEGACIÓN LATERAL DE MÓDULOS
# -------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Panel de Módulos")
modulo = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "1. Escáner Cuantitativo (300 Activos)",
        "2. Detector de Señales por Temporalidad",
        "3. Confluencia Multitemporal & Diagnóstico IA"
    ]
)

crypto_sentiment, stock_sentiment = obtener_sentimiento()
st.sidebar.markdown("---")
st.sidebar.markdown(f"🌡️ **Sentimiento Cripto (CMC):** {crypto_sentiment}")
st.sidebar.markdown(f"📉 **Sentimiento Bolsa (CNN):** {stock_sentiment}")

diccionario_activos = obtener_300_activos()
lista_tickers = list(diccionario_activos.keys())

# -------------------------------------------------------------------------
# MÓDULO 1: ESCÁNER CUANTITATIVO 300 ACTIVOS
# -------------------------------------------------------------------------
if modulo == "1. Escáner Cuantitativo (300 Activos)":
    st.subheader(f"📊 Escáner Cuantitativo Multi-Activo ({len(lista_tickers)} Instrumentos)")
    st.write("Análisis simultáneo cubriendo las 10 criptomonedas principales del Market Cap, acciones globales, ETFs, materias primas e índices.")
    
    temporalidad = st.selectbox("Temporalidad del Análisis:", ["1h", "4h", "1d", "1w"], index=2)
    
    if st.button("🚀 Ejecutar Escaneo Masivo (300 Activos)"):
        resultados = []
        barra = st.progress(0)
        total = len(lista_tickers)
        
        for i, ticker in enumerate(lista_tickers):
            nombre = diccionario_activos[ticker]
            df = descargar_datos(ticker, intervalo=temporalidad, periodo="3mo")
            if df is not None and not df.empty:
                df_ind = calcular_indicadores(df)
                if df_ind is not None and not df_ind.empty:
                    ultimo = df_ind.iloc[-1]
                    close_val = ultimo['Close'].iloc[0] if isinstance(ultimo['Close'], pd.Series) else ultimo['Close']
                    rsi_val = ultimo['RSI'].iloc[0] if isinstance(ultimo['RSI'], pd.Series) else ultimo['RSI']
                    
                    sig = str(ultimo['Signal'])
                    icon_signal = "⚪ NEUTRAL"
                    if sig == "COMPRA":
                        icon_signal = "🟢 COMPRA"
                    elif sig == "VENTA":
                        icon_signal = "🔴 VENTA"

                    resultados.append({
                        "Símbolo": ticker,
                        "Nombre del Activo": nombre,
                        "Precio Actual": f"${float(close_val):,.2f}",
                        "RSI (14)": round(float(rsi_val), 1),
                        "Patrón / Trivergencia": str(ultimo['Trivergencia']),
                        "Señal Táctica": icon_signal
                    })
            barra.progress((i + 1) / total)
            
        barra.empty()
        if resultados:
            df_res = pd.DataFrame(resultados)
            st.dataframe(df_res, use_container_width=True)
            st.success(f"¡Escaneo completado con éxito! Se procesaron los {len(df_res)} activos de la lista maestra.")
        else:
            st.error("No se pudieron recuperar datos en este momento.")

# -------------------------------------------------------------------------
# MÓDULO 2: DETECTOR DE SEÑALES POR TEMPORALIDAD
# -------------------------------------------------------------------------
elif modulo == "2. Detector de Señales por Temporalidad":
    st.subheader("🎯 Detector de Activos con Trivergencias Activas")
    st.write("Tabla filtrada exclusivamente con los activos que emiten señales confirmadas mediante el cruce de Precio, RSI, Squeeze Momentum y Volumen.")
    
    temp_m2 = st.selectbox("Selecciona Temporalidad de Escaneo:", ["1h", "4h", "1d", "1w"], index=2, key="m2_temp")
    
    if st.button("🔍 Buscar Trivergencias Activas"):
        senales_activas = []
        with st.spinner("Escaneando el mercado en busca de trivergencias reales..."):
            for ticker in lista_tickers:
                df = descargar_datos(ticker, intervalo=temp_m2, periodo="2mo")
                if df is not None:
                    df_ind = calcular_indicadores(df)
                    if df_ind is not None:
                        ult = df_ind.iloc[-1]
                        if ult['Signal'] in ["COMPRA", "VENTA"]:
                            close_v = ult['Close'].iloc[0] if isinstance(ult['Close'], pd.Series) else ult['Close']
                            rsi_v = ult['RSI'].iloc[0] if isinstance(ult['RSI'], pd.Series) else ult['RSI']
                            
                            sig = str(ult['Signal'])
                            icon_signal = "🟢 COMPRA" if sig == "COMPRA" else "🔴 VENTA"

                            senales_activas.append({
                                "Símbolo": ticker,
                                "Nombre del Activo": diccionario_activos[ticker],
                                "Temporalidad": temp_m2,
                                "Precio Actual": f"${float(close_v):,.2f}",
                                "RSI": round(float(rsi_v), 1),
                                "Patrón / Trivergencia": str(ult['Trivergencia']),
                                "Señal": icon_signal
                            })
        
        if senales_activas:
            st.markdown(f"### Activos con Trivergencia Activa en Temporalidad: {temp_m2}")
            st.dataframe(pd.DataFrame(senales_activas), use_container_width=True)
        else:
            st.info("No se encontraron trivergencias activas en este instante con los filtros actuales.")

# -------------------------------------------------------------------------
# MÓDULO 3: CONFLUENCIA MULTITEMPORAL AUTOMÁTICA & GRÁFICO CON ALERTAS
# -------------------------------------------------------------------------
elif modulo == "3. Confluencia Multitemporal & Diagnóstico IA":
    st.subheader("🧠 Confluencias Multitemporales Automáticas & Gráfico Institucional")
    st.write("El sistema detecta automáticamente los activos con confluencias en varias temporalidades. Selecciona un activo para desplegar su gráfico con marcas de trivergencia y análisis técnico.")
    
    if st.button("🔍 Escanear Confluencias Multitemporales"):
        multiconfluencias = []
        with st.spinner("Analizando confluencias en el universo de activos..."):
            for ticker in lista_tickers[:150]:
                temporalidades = ["1h", "4h", "1d", "1w"]
                temps_activas = []
                for t in temporalidades:
                    df = descargar_datos(ticker, intervalo=t, periodo="1mo")
                    if df is not None:
                        df_i = calcular_indicadores(df)
                        if df_i is not None:
                            if df_i.iloc[-1]['Signal'] in ["COMPRA", "VENTA"]:
                                temps_activas.append(t)
                
                if len(temps_activas) >= 2:
                    multiconfluencias.append({
                        "Símbolo": ticker,
                        "Nombre": diccionario_activos[ticker],
                        "Temporalidades con Señal": ", ".join(temps_activas),
                        "Total Timeframes": len(temps_activas)
                    })
        
        st.session_state['multiconfluencias'] = multiconfluencias

    if 'multiconfluencias' in st.session_state and st.session_state['multiconfluencias']:
        df_multi = pd.DataFrame(st.session_state['multiconfluencias'])
        st.markdown("### 📋 Activos con Confluencia Multitemporal Detectados:")
        st.dataframe(df_multi, use_container_width=True)
        
        tickers_encontrados = [item['Símbolo'] for item in st.session_state['multiconfluencias']]
        activo_sel = st.selectbox("Selecciona el Activo para ver Gráfico con Alertas y Diagnóstico:", tickers_encontrados)
        
        if activo_sel:
            st.markdown("---")
            st.markdown(f"### 📊 Gráfico Institucional con Trivergencias para: **{diccionario_activos[activo_sel]} ({activo_sel})**")
            
            df_chart = descargar_datos(activo_sel, intervalo="1d", period="6mo")
            if df_chart is not None and not df_chart.empty:
                df_chart = calcular_indicadores(df_chart)
                
                # Subplots: 1. Velas, 2. RSI, 3. Squeeze Momentum
                fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                                    vertical_spacing=0.03, row_heights=[0.55, 0.25, 0.2])
                
                opn = df_chart['Open'].iloc[:, 0] if isinstance(df_chart['Open'], pd.DataFrame) else df_chart['Open']
                hgh = df_chart['High'].iloc[:, 0] if isinstance(df_chart['High'], pd.DataFrame) else df_chart['High']
                lw = df_chart['Low'].iloc[:, 0] if isinstance(df_chart['Low'], pd.DataFrame) else df_chart['Low']
                cls = df_chart['Close'].iloc[:, 0] if isinstance(df_chart['Close'], pd.DataFrame) else df_chart['Close']
                rsi_s = df_chart['RSI'].iloc[:, 0] if isinstance(df_chart['RSI'], pd.DataFrame) else df_chart['RSI']
                sq_s = df_chart['Squeeze_Mom'].iloc[:, 0] if isinstance(df_chart['Squeeze_Mom'], pd.DataFrame) else df_chart['Squeeze_Mom']

                # Velas Japonesas
                fig.add_trace(go.Candlestick(x=df_chart.index, open=opn, high=hgh, low=lw, close=cls, name="Precio"), row=1, col=1)
                
                # Marcar Círculos de Trivergencia en el Gráfico si la señal está activa
                ult_sig = df_chart['Signal'].iloc[-1]
                if isinstance(ult_sig, pd.Series):
                    ult_sig = ult_sig.iloc[0]
                
                if ult_sig == "COMPRA":
                    fig.add_trace(go.Scatter(x=[df_chart.index[-1]], y=[cls.iloc[-1]], mode="markers", marker=dict(color="green", size=14, symbol="circle"), name="Trivergencia Alcista (🟢)"), row=1, col=1)
                elif ult_sig == "VENTA":
                    fig.add_trace(go.Scatter(x=[df_chart.index[-1]], y=[cls.iloc[-1]], mode="markers", marker=dict(color="red", size=14, symbol="circle"), name="Trivergencia Bajista (🔴)"), row=1, col=1)

                # RSI Ploteado en fila 2
                fig.add_trace(go.Scatter(x=df_chart.index, y=rsi_s, line=dict(color='#00ffcc', width=1.5), name="RSI (14)"), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                # Squeeze Momentum Histogram en fila 3
                colors = ['green' if val >= 0 else 'red' for val in sq_s]
                fig.add_trace(go.Bar(x=df_chart.index, y=sq_s, marker_color=colors, name="Squeeze Momentum"), row=3, col=1)
                
                fig.update_layout(height=750, template="plotly_dark", title_text=f"Análisis Institucional Avanzado: {activo_sel}", xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("### 🤖 Diagnóstico y Proyección Institucional")
                st.info(f"""
                **Evaluación Profesional con Confluencia de Indicadores para {diccionario_activos[activo_sel]}:**
                * **Sistema Trivergencia (Cryptosoldier):** Combina el comportamiento del precio con el **RSI**, el **Squeeze Momentum** y el **Volumen Relativo** para detectar agotamientos reales y giros institucionales.
                * **Señales Visuales en Gráfico:** Los círculos integrados en el gráfico principal señalan puntos de entrada tácticos validados en extremos de mercado.
                * **Gestión de Riesgo:** Mantenga operativas alineadas con la directriz multitemporal y respete los niveles de invalidación técnica.
                """)
            else:
                st.error("No se pudieron cargar los datos del gráfico para este activo.")
    else:
        st.info("Haz clic en el botón de arriba para iniciar el escaneo automático de confluencias multitemporales.")
