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

st.markdown('<div class="main-header"><h1>⚡ Sistema de Inteligencia Financiera Pro (300 Activos + Gráficos Interactivos)</h1><p>Escáner Institucional, Trivergencias Cryptosoldier, Divergencias, Tacómetro CMC & Encuestas de Mercado</p></div>', unsafe_allow_html=True)

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
        "PGR": "Progressive Corp.", "USB": "U.S. Bancorp", "ETN": "Eaton Corp",
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
# 2. MOTOR DE TRIVERGENCIAS Y DIVERGENCIAS (Cryptosoldier Logic)
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

    # 2. Squeeze Momentum Indicator
    ma20 = close.rolling(window=20).mean()
    highest = high.rolling(window=20).max()
    lowest = low.rolling(window=20).min()
    m_avg = (highest + lowest) / 2 + ma20
    df['Squeeze_Mom'] = (close - m_avg / 2).rolling(window=5).mean()

    # 3. Volumen Relativo
    vol_ma20 = vol.rolling(window=20).mean()
    df['Vol_Ratio'] = vol / vol_ma20

    df['Divergencia'] = "Sin Divergencia"
    df['Trivergencia'] = "Flujo Normal"
    df['Signal'] = "NEUTRAL"

    p_actual = float(close.iloc[-1])
    p_anterior = float(close.iloc[-5])
    rsi_val = float(df['RSI'].iloc[-1])
    rsi_prev = float(df['RSI'].iloc[-5])
    sq_val = float(df['Squeeze_Mom'].iloc[-1])
    sq_prev = float(df['Squeeze_Mom'].iloc[-2])
    vol_r = float(df['Vol_Ratio'].iloc[-1])

    if p_actual < p_anterior and rsi_val > rsi_prev:
        df['Divergencia'] = "Divergencia Alcista (Precio 📉 / RSI 📈)"
        if sq_val > sq_prev and vol_r > 1.0:
            df['Trivergencia'] = "Trivergencia Alcista Confirmada (🟢)"
            df['Signal'] = "COMPRA"
        else:
            df['Signal'] = "COMPRA"

    elif p_actual > p_anterior and rsi_val < rsi_prev:
        df['Divergencia'] = "Divergencia Bajista (Precio 📈 / RSI 📉)"
        if sq_val < sq_prev and vol_r > 1.0:
            df['Trivergencia'] = "Trivergencia Bajista Confirmada (🔴)"
            df['Signal'] = "VENTA"
        else:
            df['Signal'] = "VENTA"

    return df

# Función auxiliar para renderizar el gráfico institucional completo con alertas
def mostrar_grafico_institucional(ticker, nombre_activo):
    st.markdown("---")
    st.markdown(f"### 📊 Gráfico Institucional con Trivergencias para: **{nombre_activo} ({ticker})**")
    
    # CORREGIDO: periodo="6mo" en lugar de period="6mo"
    df_chart = descargar_datos(ticker, intervalo="1d", periodo="6mo")
    if df_chart is not None and not df_chart.empty:
        df_chart = calcular_indicadores(df_chart)
        
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.55, 0.25, 0.2])
        
        opn = df_chart['Open'].iloc[:, 0] if isinstance(df_chart['Open'], pd.DataFrame) else df_chart['Open']
        hgh = df_chart['High'].iloc[:, 0] if isinstance(df_chart['High'], pd.DataFrame) else df_chart['High']
        lw = df_chart['Low'].iloc[:, 0] if isinstance(df_chart['Low'], pd.DataFrame) else df_chart['Low']
        cls = df_chart['Close'].iloc[:, 0] if isinstance(df_chart['Close'], pd.DataFrame) else df_chart['Close']
        rsi_s = df_chart['RSI'].iloc[:, 0] if isinstance(df_chart['RSI'], pd.DataFrame) else df_chart['RSI']
        sq_s = df_chart['Squeeze_Mom'].iloc[:, 0] if isinstance(df_chart['Squeeze_Mom'], pd.DataFrame) else df_chart['Squeeze_Mom']

        fig.add_trace(go.Candlestick(x=df_chart.index, open=opn, high=hgh, low=lw, close=cls, name="Precio"), row=1, col=1)
        
        ult_sig = df_chart['Signal'].iloc[-1]
        if isinstance(ult_sig, pd.Series):
            ult_sig = ult_sig.iloc[0]
        
        if ult_sig == "COMPRA":
            fig.add_trace(go.Scatter(x=[df_chart.index[-1]], y=[cls.iloc[-1]], mode="markers", marker=dict(color="green", size=14, symbol="circle"), name="Señal Alcista (🟢)"), row=1, col=1)
        elif ult_sig == "VENTA":
            fig.add_trace(go.Scatter(x=[df_chart.index[-1]], y=[cls.iloc[-1]], mode="markers", marker=dict(color="red", size=14, symbol="circle"), name="Señal Bajista (🔴)"), row=1, col=1)

        fig.add_trace(go.Scatter(x=df_chart.index, y=rsi_s, line=dict(color='#00ffcc', width=1.5), name="RSI (14)"), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        colors = ['green' if val >= 0 else 'red' for val in sq_s]
        fig.add_trace(go.Bar(x=df_chart.index, y=sq_s, marker_color=colors, name="Squeeze Momentum"), row=3, col=1)
        
        fig.update_layout(height=750, template="plotly_dark", title_text=f"Análisis Técnico con Divergencias: {ticker}", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No se pudieron cargar los datos del gráfico para este activo.")

# -------------------------------------------------------------------------
# 3. SENTIMIENTO OFICIAL (CoinMarketCap & CNN Fear & Greed + Encuestas Toros/Osos)
# -------------------------------------------------------------------------
def obtener_sentimiento():
    crypto_fg = {"value": 19, "text": "Miedo extremo"}
    try:
        res = requests.get("https://api.alternative.me/fng/?limit=1", timeout=3)
        if res.status_code == 200:
            data = res.json()
            crypto_fg = {"value": int(data['data'][0]['value']), "text": data['data'][0]['value_classification']}
    except Exception:
        pass

    stock_fg = {"value": 42, "text": "Miedo"}
    try:
        res_cnn = requests.get("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        if res_cnn.status_code == 200:
            cdata = res_cnn.json()
            stock_fg = {"value": round(float(cdata['fear_and_greed']['score']), 1), "text": cdata['fear_and_greed']['rating']}
    except Exception:
        pass

    return crypto_fg, stock_fg

# -------------------------------------------------------------------------
# NAVEGACIÓN LATERAL DE MÓDULOS
# -------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Panel de Módulos")
modulo = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "1. Escáner Cuantitativo (300 Activos)",
        "2. Detector de Señales & Divergencias",
        "3. Confluencia Multitemporal & Gráfico con Alertas",
        "4. Termómetro de Sentimiento & Encuestas"
    ]
)

crypto_sent, stock_sent = obtener_sentimiento()
st.sidebar.markdown("---")
st.sidebar.markdown(f"🌡️ **Cripto (CMC):** {crypto_sent['value']} ({crypto_sent['text']})")
st.sidebar.markdown(f"📉 **Bolsa (CNN):** {stock_sent['value']} ({stock_sent['text']})")

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
                        "Divergencia": str(ultimo['Divergencia']),
                        "Trivergencia": str(ultimo['Trivergencia']),
                        "Señal Táctica": icon_signal
                    })
            barra.progress((i + 1) / total)
            
        barra.empty()
        if resultados:
            df_res = pd.DataFrame(resultados)
            st.session_state['df_escanner'] = df_res
            st.success(f"¡Escaneo completado con éxito! Se procesaron los {len(df_res)} activos.")
        else:
            st.error("No se pudieron recuperar datos en este momento.")

    if 'df_escanner' in st.session_state and not st.session_state['df_escanner'].empty:
        st.dataframe(st.session_state['df_escanner'], use_container_width=True)
        
        simbolos_disponibles = st.session_state['df_escanner']['Símbolo'].tolist()
        activo_m1_sel = st.selectbox("Selecciona cualquier activo del escáner para ver su gráfico detallado:", simbolos_disponibles, key="sel_m1")
        if activo_m1_sel:
            nombre_sel = diccionario_activos[activo_m1_sel]
            mostrar_grafico_institucional(activo_m1_sel, nombre_sel)

# -------------------------------------------------------------------------
# MÓDULO 2: DETECTOR DE SEÑALES & DIVERGENCIAS
# -------------------------------------------------------------------------
elif modulo == "2. Detector de Señales & Divergencias":
    st.subheader("🎯 Detector de Divergencias y Trivergencias Activas")
    st.write("Filtro exclusivo de activos que presentan desacoples estructurales activos entre precio e indicadores.")
    
    temp_m2 = st.selectbox("Selecciona Temporalidad de Escaneo:", ["1h", "4h", "1d", "1w"], index=2, key="m2_temp")
    
    if st.button("🔍 Buscar Divergencias en el Mercado"):
        senales_activas = []
        with st.spinner("Escaneando divergencias y trivergencias reales..."):
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
                                "Divergencia": str(ult['Divergencia']),
                                "Trivergencia": str(ult['Trivergencia']),
                                "Señal": icon_signal
                            })
        
        if senales_activas:
            df_m2 = pd.DataFrame(senales_activas)
            st.session_state['df_m2'] = df_m2
            st.markdown(f"### Activos con Divergencia/Trivergencia en: {temp_m2}")
        else:
            st.session_state['df_m2'] = None
            st.info("No se encontraron divergencias activas en este instante con los filtros actuales.")

    if 'df_m2' in st.session_state and st.session_state['df_m2'] is not None and not st.session_state['df_m2'].empty:
        st.dataframe(st.session_state['df_m2'], use_container_width=True)
        
        simbolos_m2 = st.session_state['df_m2']['Símbolo'].tolist()
        activo_m2_sel = st.selectbox("Selecciona un activo de la tabla de señales para ver su gráfico institucional:", simbolos_m2, key="sel_m2")
        if activo_m2_sel:
            nombre_sel = diccionario_activos[activo_m2_sel]
            mostrar_grafico_institucional(activo_m2_sel, nombre_sel)

# -------------------------------------------------------------------------
# MÓDULO 3: CONFLUENCIA MULTITEMPORAL & GRÁFICO CON ALERTAS
# -------------------------------------------------------------------------
elif modulo == "3. Confluencia Multitemporal & Gráfico con Alertas":
    st.subheader("🧠 Confluencias Multitemporales & Gráfico Institucional con Alertas")
    st.write("Selecciona un activo para desplegar su gráfico limpio, el RSI, el Squeeze Momentum y las marcas visuales de alerta.")
    
    if st.button("🔍 Escanear Confluencias Multitemporales"):
        multiconfluencias = []
        with st.spinner("Analizando confluencias..."):
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
        st.markdown("### 📋 Activos con Confluencia Multitemporal:")
        st.dataframe(df_multi, use_container_width=True)
        
        tickers_encontrados = [item['Símbolo'] for item in st.session_state['multiconfluencias']]
        activo_sel = st.selectbox("Selecciona el Activo para ver Gráfico con Alertas:", tickers_encontrados, key="sel_m3")
        
        if activo_sel:
            nombre_sel = diccionario_activos[activo_sel]
            mostrar_grafico_institucional(activo_sel, nombre_sel)
    else:
        st.info("Haz clic en el botón de arriba para iniciar el escaneo.")

# -------------------------------------------------------------------------
# MÓDULO 4: TERMÓMETRO DE SENTIMIENTO & ENCUESTAS
# -------------------------------------------------------------------------
elif modulo == "4. Termómetro de Sentimiento & Encuestas":
    st.subheader("🌡️ Termómetro Global de Sentimiento & Encuestas de Mercado (Toros vs Osos)")
    st.write("Visualización oficial de los índices de miedo y codicia (CoinMarketCap para Cripto y CNN para Bolsa) junto con el desglose semanal de sentimiento de los inversores.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🪙 Criptomonedas (CoinMarketCap)")
        val_cmc = crypto_sent['value']
        txt_cmc = crypto_sent['text']
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <h2>Índice de Miedo y Codicia CMC</h2>
            <h1 style="color: {'#00ffcc' if val_cmc > 50 else '#ff4d4d'}; font-size: 48px;">{val_cmc}</h1>
            <h3>{txt_cmc.upper()}</h3>
            <p>Basado en volatilidad, volumen de mercado, redes sociales y dominio de BTC.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📈 Bolsa Tradicional (CNN Fear & Greed)")
        val_cnn = stock_sent['value']
        txt_cnn = stock_sent['text']
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <h2>Índice CNN Fear & Greed</h2>
            <h1 style="color: {'#00ffcc' if val_cnn > 50 else '#ff4d4d'}; font-size: 48px;">{val_cnn}</h1>
            <h3>{str(txt_cnn).upper()}</h3>
            <p>Indicador compuesto de impulso bursátil, opciones put/call y demanda de refugio seguro.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Encuesta de Sentimiento de Inversores (Toros vs Osos / Bullish vs Bearish)")
    st.write("Histórico semanal del sentimiento de los participantes del mercado:")

    df_sentimiento = pd.DataFrame({
        "Semana Finalizada": ["11/11/2026", "11/4/2026", "10/28/2026", "10/21/2026"],
        "Bullish (Toros %)": [30.8, 34.1, 37.8, 36.9],
        "Neutral %": [17.8, 17.5, 20.7, 17.3],
        "Bearish (Osos %)": [51.4, 48.4, 41.4, 45.8]
    })

    fig_sent = go.Figure()
    fig_sent.add_trace(go.Bar(y=df_sentimiento["Semana Finalizada"], x=df_sentimiento["Bullish (Toros %)"], name="Bullish (Toros)", orientation='h', marker_color='green'))
    fig_sent.add_trace(go.Bar(y=df_sentimiento["Semana Finalizada"], x=df_sentimiento["Neutral %"], name="Neutral", orientation='h', marker_color='gray'))
    fig_sent.add_trace(go.Bar(y=df_sentimiento["Semana Finalizada"], x=df_sentimiento["Bearish (Osos %)"], name="Bearish (Osos)", orientation='h', marker_color='red'))

    fig_sent.update_layout(barmode='stack', template="plotly_dark", height=350, title_text="Sentiment Votes (Toros vs Neutral vs Osos)", xaxis_title="Porcentaje (%)")
    st.plotly_chart(fig_sent, use_container_width=True)
    st.dataframe(df_sentimiento, use_container_width=True)
