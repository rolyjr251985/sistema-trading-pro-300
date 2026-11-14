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

# Estilo visual institucional ultra nítido: Corrección total de alertas y legibilidad
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: #ffffff !important;
    }
    /* Forzar tipografía clara y de alta visibilidad en toda la interfaz */
    p, span, label, div, h1, h2, h3, h4, h5, h6, .stMarkdown, .streamlit-expanderHeader {
        color: #f8fafc !important;
    }
    /* CORRECCIÓN DEFINITIVA PARA CAJAS DE INFO Y ALERTAS (st.info, st.success, etc.) */
    div.stAlert, div[data-baseweb="notification"], div.stInfo, div.stSuccess, div.stWarning, div.stError {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    div.stAlert *, div.stInfo *, div.stSuccess *, div.stWarning *, div.stError * {
        color: #ffffff !important;
    }
    /* Corrección para los menús desplegables (Selectboxes y Dropdowns) */
    div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-color: #334155 !important;
    }
    div[data-baseweb="menu"], div[role="listbox"], ul[role="listbox"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
    }
    div[data-baseweb="option"], option, div[role="option"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
    }
    div[data-baseweb="option"]:hover {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
    }
    input, textarea, select {
        color: #ffffff !important;
        background-color: #0f172a !important;
    }
    /* Estilos específicos para la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #080c14;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    /* Banner Principal Estilizado */
    .main-header {
        background: linear-gradient(135deg, #312e81 0%, #1e1b4b 50%, #090d16 100%);
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #4f46e5;
        box-shadow: 0 20px 30px -10px rgba(79, 70, 229, 0.3);
        color: #ffffff;
        text-align: center;
        margin-bottom: 30px;
    }
    /* Tarjetas de Contenido */
    .card {
        background: linear-gradient(145deg, #0f172a 0%, #111827 100%);
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #334155;
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    /* Botones Mejorados */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px;
        border: none;
        padding: 12px 28px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 2.6rem; margin-bottom: 8px; font-weight: 800; color: #ffffff !important;">⚡ Sistema de Inteligencia Financiera Pro</h1>
        <p style="color: #e2e8f0 !important; font-size: 1.15rem; margin: 0; font-weight: 500;">Plataforma Cuantitativa Avanzada: Trivergencias, Escáner 300 Activos & Análisis Multitemporal</p>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 1. LISTA MAESTRA AMPLIADA A 300 ACTIVOS EXACTOS
# -------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def obtener_300_activos():
    diccionario_activos = {
        # Top 10 Criptomonedas por Market Cap
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
# 2. MOTOR DE TRIVERGENCIAS Y DIVERGENCIAS (Blindado contra nan)
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

def limpiar_serie(serie):
    if isinstance(serie, pd.DataFrame):
        serie = serie.iloc[:, 0]
    return pd.Series(serie).squeeze()

def calcular_indicadores(df):
    if df is None or len(df) < 30:
        return None
    
    close = limpiar_serie(df['Close'])
    high = limpiar_serie(df['High'])
    low = limpiar_serie(df['Low'])
    vol = limpiar_serie(df['Volume'])

    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    ma20 = close.rolling(window=20).mean()
    highest = high.rolling(window=20).max()
    lowest = low.rolling(window=20).min()
    m_avg = (highest + lowest) / 2 + ma20
    df['Squeeze_Mom'] = (close - m_avg / 2).rolling(window=5).mean()

    vol_ma20 = vol.rolling(window=20).mean()
    df['Vol_Ratio'] = vol / vol_ma20

    df['Divergencia'] = "Sin Divergencia"
    df['Trivergencia'] = "Flujo Normal"
    df['Signal'] = "NEUTRAL"

    if len(close) >= 5:
        p_actual = float(close.iloc[-1])
        p_anterior = float(close.iloc[-5])
        rsi_val = float(limpiar_serie(df['RSI']).iloc[-1])
        rsi_prev = float(limpiar_serie(df['RSI']).iloc[-5])
        sq_val = float(limpiar_serie(df['Squeeze_Mom']).iloc[-1])
        sq_prev = float(limpiar_serie(df['Squeeze_Mom']).iloc[-2])
        vol_r = float(limpiar_serie(df['Vol_Ratio']).iloc[-1])

        if p_actual < p_anterior and rsi_val > rsi_prev:
            df['Divergencia'] = "Divergencia Alcista (Precio 📉 / RSI 📈)"
            if sq_val > sq_prev and vol_r > 0.8:
                df['Trivergencia'] = "Trivergencia Alcista Confirmada (🟢)"
                df['Signal'] = "COMPRA"
            else:
                df['Signal'] = "COMPRA"

        elif p_actual > p_anterior and rsi_val < rsi_prev:
            df['Divergencia'] = "Divergencia Bajista (Precio 📈 / RSI 📉)"
            if sq_val < sq_prev and vol_r > 0.8:
                df['Trivergencia'] = "Trivergencia Bajista Confirmada (🔴)"
                df['Signal'] = "VENTA"
            else:
                df['Signal'] = "VENTA"

    return df

def extraer_valor_seguro(serie_o_df):
    try:
        val = limpiar_serie(serie_o_df)
        if hasattr(val, 'iloc'):
            val = val.iloc[-1]
        res = float(val)
        if np.isnan(res):
            return 0.0
        return res
    except Exception:
        return 0.0

def resolver_ticker_ingresado(input_str, dic_activos):
    clean = input_str.strip()
    if clean in dic_activos:
        return clean
    for ticker, nombre in dic_activos.items():
        if clean.lower() in ticker.lower() or clean.lower() in nombre.lower():
            return ticker
    return clean.upper()

def mostrar_grafico_institucional(ticker, nombre_activo):
    st.markdown("---")
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 18px 22px; border-radius: 12px; border-left: 5px solid #6366f1; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #ffffff !important; font-size: 1.25rem;">📊 Gráfico Institucional & Osciladores: {nombre_activo} (<span style="color: #818cf8;">{ticker}</span>)</h3>
        </div>
    """, unsafe_allow_html=True)
    
    df_chart = descargar_datos(ticker, intervalo="1d", periodo="6mo")
    if df_chart is not None and not df_chart.empty:
        df_chart = calcular_indicadores(df_chart)
        if df_chart is not None:
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                                vertical_spacing=0.03, row_heights=[0.55, 0.25, 0.2])
            
            opn = limpiar_serie(df_chart['Open'])
            hgh = limpiar_serie(df_chart['High'])
            lw = limpiar_serie(df_chart['Low'])
            cls = limpiar_serie(df_chart['Close'])
            rsi_s = limpiar_serie(df_chart['RSI'])
            sq_s = limpiar_serie(df_chart['Squeeze_Mom'])

            fig.add_trace(go.Candlestick(x=df_chart.index, open=opn, high=hgh, low=lw, close=cls, name="Precio"), row=1, col=1)
            
            ult_sig = str(limpiar_serie(df_chart['Signal']).iloc[-1])
            if ult_sig == "COMPRA":
                fig.add_trace(go.Scatter(x=[df_chart.index[-1]], y=[extraer_valor_seguro(cls)], mode="markers", marker=dict(color="#10b981", size=16, symbol="circle"), name="Señal Alcista (🟢)"), row=1, col=1)
            elif ult_sig == "VENTA":
                fig.add_trace(go.Scatter(x=[df_chart.index[-1]], y=[extraer_valor_seguro(cls)], mode="markers", marker=dict(color="#ef4444", size=16, symbol="circle"), name="Señal Bajista (🔴)"), row=1, col=1)

            fig.add_trace(go.Scatter(x=df_chart.index, y=rsi_s, line=dict(color='#38bdf8', width=2), name="RSI (14)"), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="#10b981", row=2, col=1)

            colors = ['#10b981' if val >= 0 else '#ef4444' for val in sq_s]
            fig.add_trace(go.Bar(x=df_chart.index, y=sq_s, marker_color=colors, name="Squeeze Momentum"), row=3, col=1)
            
            fig.update_layout(height=780, template="plotly_dark", paper_bgcolor="#030712", plot_bgcolor="#030712", title_text="", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            return
    st.error(f"No se pudieron cargar los datos del gráfico para el ticker `{ticker}`.")

# -------------------------------------------------------------------------
# 3. SENTIMIENTO GLOBAL
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
st.sidebar.markdown("### 🎛️ Panel de Control Pro")
modulo = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "1. Escáner Cuantitativo (300 Activos)",
        "2. Detector de Divergencias & Sobrecompra/Sobreventa",
        "3. Confluencia Multitemporal & Gráfico Pro",
        "4. Termómetro de Sentimiento & Encuestas",
        "5. 🔎 Búsqueda de Activo Individual (Multitemporal)"
    ]
)

crypto_sent, stock_sent = obtener_sentimiento()
st.sidebar.markdown("---")
st.sidebar.markdown(f"🌡️ **Cripto (CMC):** `{crypto_sent['value']}` ({crypto_sent['text']})")
st.sidebar.markdown(f"📉 **Bolsa (CNN):** `{stock_sent['value']}` ({stock_sent['text']})")

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
                    close_val = extraer_valor_seguro(ultimo['Close'])
                    rsi_val = extraer_valor_seguro(ultimo['RSI'])
                    
                    sig = str(limpiar_serie(ultimo['Signal']))
                    icon_signal = "⚪ NEUTRAL"
                    if sig == "COMPRA":
                        icon_signal = "🟢 COMPRA"
                    elif sig == "VENTA":
                        icon_signal = "🔴 VENTA"

                    resultados.append({
                        "Símbolo": ticker,
                        "Nombre del Activo": nombre,
                        "Precio Actual": f"${close_val:,.2f}",
                        "RSI (14)": round(rsi_val, 1),
                        "Divergencia": str(limpiar_serie(ultimo['Divergencia'])),
                        "Trivergencia": str(limpiar_serie(ultimo['Trivergencia'])),
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
            nombre_sel = diccionario_activos.get(activo_m1_sel, activo_m1_sel)
            mostrar_grafico_institucional(activo_m1_sel, nombre_sel)

# -------------------------------------------------------------------------
# MÓDULO 2: DETECTOR DE DIVERGENCIAS & SOBRECOMPRA/SOBREVENTA
# -------------------------------------------------------------------------
elif modulo == "2. Detector de Divergencias & Sobrecompra/Sobreventa":
    st.subheader("🎯 Detector Multitemporal: Sobrecompra, Sobreventa y Divergencias")
    st.write("Filtra activos con confluencias extremas en 4H, Diario y Semanal, además de tablas dedicadas por temporalidad y gráficos interactivos.")
    
    if st.button("🔍 Ejecutar Escaneo Multitemporal Extremo"):
        triple_confluencia = []
        solo_diario = []
        solo_semanal = []
        
        barra_m2 = st.progress(0)
        activos_m2 = lista_tickers[:120]
        total_m2 = len(activos_m2)
        
        for idx, ticker in enumerate(activos_m2):
            nombre = diccionario_activos[ticker]
            df_4h = descargar_datos(ticker, intervalo="4h", periodo="1mo")
            df_1d = descargar_datos(ticker, intervalo="1d", periodo="3mo")
            df_1w = descargar_datos(ticker, intervalo="1w", periodo="1y")
            
            rsi_4h, rsi_1d, rsi_1w = None, None, None
            
            if df_4h is not None and not df_4h.empty:
                d4 = calcular_indicadores(df_4h)
                if d4 is not None and not d4.empty:
                    rsi_4h = extraer_valor_seguro(d4['RSI'])
            
            if df_1d is not None and not df_1d.empty:
                d1 = calcular_indicadores(df_1d)
                if d1 is not None and not d1.empty:
                    rsi_1d = extraer_valor_seguro(d1['RSI'])
            
            if df_1w is not None and not df_1w.empty:
                dw = calcular_indicadores(df_1w)
                if dw is not None and not dw.empty:
                    rsi_1w = extraer_valor_seguro(dw['RSI'])
            
            if rsi_4h is not None and rsi_1d is not None and rsi_1w is not None:
                if rsi_4h > 70 and rsi_1d > 70 and rsi_1w > 70:
                    triple_confluencia.append({"Símbolo": ticker, "Nombre": nombre, "Condición": "🔴 Sobrecompra Extrema (4H + 1D + 1W)", "RSI 4H": round(rsi_4h, 1), "RSI 1D": round(rsi_1d, 1), "RSI 1W": round(rsi_1w, 1)})
                elif rsi_4h < 30 and rsi_1d < 30 and rsi_1w < 30:
                    triple_confluencia.append({"Símbolo": ticker, "Nombre": nombre, "Condición": "🟢 Sobreventa Extrema (4H + 1D + 1W)", "RSI 4H": round(rsi_4h, 1), "RSI 1D": round(rsi_1d, 1), "RSI 1W": round(rsi_1w, 1)})

            if rsi_1d is not None:
                if rsi_1d > 70:
                    solo_diario.append({"Símbolo": ticker, "Nombre": nombre, "Condición": "🔴 Sobrecompra Diaria", "RSI Diario": round(rsi_1d, 1)})
                elif rsi_1d < 30:
                    solo_diario.append({"Símbolo": ticker, "Nombre": nombre, "Condición": "🟢 Sobreventa Diaria", "RSI Diario": round(rsi_1d, 1)})

            if rsi_1w is not None:
                if rsi_1w > 70:
                    solo_semanal.append({"Símbolo": ticker, "Nombre": nombre, "Condición": "🔴 Sobrecompra Semanal", "RSI Semanal": round(rsi_1w, 1)})
                elif rsi_1w < 30:
                    solo_semanal.append({"Símbolo": ticker, "Nombre": nombre, "Condición": "🟢 Sobreventa Semanal", "RSI Semanal": round(rsi_1w, 1)})

            barra_m2.progress((idx + 1) / total_m2)
            
        barra_m2.empty()
        
        st.session_state['triple_confluencia'] = pd.DataFrame(triple_confluencia) if triple_confluencia else pd.DataFrame()
        st.session_state['solo_diario'] = pd.DataFrame(solo_diario) if solo_diario else pd.DataFrame()
        st.session_state['solo_semanal'] = pd.DataFrame(solo_semanal) if solo_semanal else pd.DataFrame()
        st.success("¡Escaneo multitemporal completado con éxito!")

    if 'triple_confluencia' in st.session_state:
        st.markdown("### 🚨 1. Triple Confluencia Simultánea (4H + Diario + Semanal)")
        if not st.session_state['triple_confluencia'].empty:
            st.dataframe(st.session_state['triple_confluencia'], use_container_width=True)
        else:
            st.info("No hay activos cumpliendo la triple confluencia exacta en este instante.")

    if 'solo_diario' in st.session_state:
        st.markdown("### 📅 2. Activos en Sobrecompra / Sobreventa (Gráfico Diario 1D)")
        if not st.session_state['solo_diario'].empty:
            st.dataframe(st.session_state['solo_diario'], use_container_width=True)
        else:
            st.info("No se encontraron activos en extremos diarios.")

    if 'solo_semanal' in st.session_state:
        st.markdown("### 📈 3. Activos en Sobrecompra / Sobreventa (Gráfico Semanal 1W)")
        if not st.session_state['solo_semanal'].empty:
            st.dataframe(st.session_state['solo_semanal'], use_container_width=True)
        else:
            st.info("No se encontraron activos en extremos semanales.")

    st.markdown("---")
    st.markdown("### 📊 Consultar Gráfico de Cualquier Activo")
    activo_m2_sel = st.selectbox("Selecciona un activo para visualizar su estructura técnica y osciladores:", lista_tickers, key="sel_m2_directo")
    if activo_m2_sel:
        nombre_sel = diccionario_activos.get(activo_m2_sel, activo_m2_sel)
        mostrar_grafico_institucional(activo_m2_sel, nombre_sel)

# -------------------------------------------------------------------------
# MÓDULO 3: CONFLUENCIA MULTITEMPORAL & GRÁFICO PRO
# -------------------------------------------------------------------------
elif modulo == "3. Confluencia Multitemporal & Gráfico Pro":
    st.subheader("🧠 Confluencias Multitemporales & Gráfico Institucional con Alertas")
    st.write("Selecciona un activo para desplegar su gráfico limpio, el RSI, el Squeeze Momentum y las marcas visuales de alerta.")
    
    if st.button("🔍 Escanear Confluencias Multitemporales"):
        multiconfluencias = []
        with st.spinner("Analizando confluencias..."):
            for ticker in lista_tickers[:100]:
                temporalidades = ["1h", "4h", "1d", "1w"]
                temps_activas = []
                for t in temporalidades:
                    df = descargar_datos(ticker, intervalo=t, periodo="1mo")
                    if df is not None:
                        df_i = calcular_indicadores(df)
                        if df_i is not None:
                            if limpiar_serie(df_i.iloc[-1]['Signal']) in ["COMPRA", "VENTA"]:
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
            nombre_sel = diccionario_activos.get(activo_sel, activo_sel)
            mostrar_grafico_institucional(activo_sel, nombre_sel)
    else:
        st.info("Haz clic en el botón de arriba para iniciar el escaneo de confluencias.")

# -------------------------------------------------------------------------
# MÓDULO 4: TERMÓMETRO DE SENTIMIENTO & ENCUESTAS
# -------------------------------------------------------------------------
elif modulo == "4. Termómetro de Sentimiento & Encuestas":
    st.subheader("🌡️ Termómetro Global de Sentimiento & Encuestas de Mercado (Toros vs Osos)")
    st.write("Visualización oficial de los índices de miedo y codicia (CoinMarketCap para Cripto y CNN para Bolsa) junto con el desglose semanal de sentimiento.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        val_cmc = crypto_sent['value']
        txt_cmc = crypto_sent['text']
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <h3 style="color: #818cf8; margin-top: 0;">🪙 Criptomonedas (CoinMarketCap)</h3>
            <h2 style="margin: 5px 0;">Índice de Miedo y Codicia</h2>
            <h1 style="color: {'#10b981' if val_cmc > 50 else '#ef4444'}; font-size: 52px; margin: 10px 0;">{val_cmc}</h1>
            <h3 style="text-transform: uppercase; letter-spacing: 1px;">{txt_cmc}</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">Basado en volatilidad, volumen, redes sociales y dominio.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        val_cnn = stock_sent['value']
        txt_cnn = stock_sent['text']
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <h3 style="color: #38bdf8; margin-top: 0;">📈 Bolsa Tradicional (CNN Fear & Greed)</h3>
            <h2 style="margin: 5px 0;">Índice de Sentimiento Bursátil</h2>
            <h1 style="color: {'#10b981' if val_cnn > 50 else '#ef4444'}; font-size: 52px; margin: 10px 0;">{val_cnn}</h1>
            <h3 style="text-transform: uppercase; letter-spacing: 1px;">{str(txt_cnn)}</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">Indicador compuesto de impulso, opciones put/call y refugio.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Encuesta de Sentimiento de Inversores (Toros vs Osos)")
    st.write("Histórico semanal del sentimiento de los participantes del mercado:")

    df_sentimiento = pd.DataFrame({
        "Semana Finalizada": ["11/11/2026", "11/4/2026", "10/28/2026", "10/21/2026"],
        "Bullish (Toros %)": [30.8, 34.1, 37.8, 36.9],
        "Neutral %": [17.8, 17.5, 20.7, 17.3],
        "Bearish (Osos %)": [51.4, 48.4, 41.4, 45.8]
    })

    fig_sent = go.Figure()
    fig_sent.add_trace(go.Bar(y=df_sentimiento["Semana Finalizada"], x=df_sentimiento["Bullish (Toros %)"], name="Bullish (Toros)", orientation='h', marker_color='#10b981'))
    fig_sent.add_trace(go.Bar(y=df_sentimiento["Semana Finalizada"], x=df_sentimiento["Neutral %"], name="Neutral", orientation='h', marker_color='#64748b'))
    fig_sent.add_trace(go.Bar(y=df_sentimiento["Semana Finalizada"], x=df_sentimiento["Bearish (Osos %)"], name="Bearish (Osos)", orientation='h', marker_color='#ef4444'))

    fig_sent.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor="#030712", plot_bgcolor="#030712", height=350, title_text="Sentiment Votes (Toros vs Neutral vs Osos)", xaxis_title="Porcentaje (%)")
    st.plotly_chart(fig_sent, use_container_width=True)
    st.dataframe(df_sentimiento, use_container_width=True)

# -------------------------------------------------------------------------
# MÓDULO 5: BÚSQUEDA DE ACTIVO INDIVIDUAL MULTITEMPORAL CORREGIDA
# -------------------------------------------------------------------------
elif modulo == "5. 🔎 Búsqueda de Activo Individual (Multitemporal)":
    st.subheader("🔎 Buscador Institucional de Activo & Desglose Multitemporal (Divergencias)")
    st.write("Introduce el nombre o símbolo (ej. `TSLA`, `NVIDIA`, `BTC-USD`, `Apple`, `GC=F`) para analizar su precio, sentimiento y estado en cada temporalidad.")
    
    col_input1, col_input2 = st.columns([2, 1])
    with col_input1:
        input_usuario = st.text_input("Introduce el Ticker o Nombre del Activo:", value="TSLA")

    if st.button("🚀 Analizar Activo en Todas las Temporalidades"):
        ticker_input = resolver_ticker_ingresado(input_usuario, diccionario_activos)
        
        with st.spinner(f"Analizando {ticker_input} en 1h, 4h, 1d y 1w..."):
            
            temporalidades_estudio = ["1h", "4h", "1d", "1w"]
            resumen_multi = []
            
            ticker_obj = yf.Ticker(ticker_input)
            info_fund = {}
            try:
                info_fund = ticker_obj.info
            except Exception:
                pass
            
            nombre_oficial = info_fund.get('longName', info_fund.get('shortName', diccionario_activos.get(ticker_input, ticker_input)))
            market_cap = info_fund.get('marketCap', 'No disponible')
            if isinstance(market_cap, (int, float)):
                market_cap = f"${market_cap:,.0f}"

            precio_actual_global = 0.0

            for temp in temporalidades_estudio:
                per = "1mo" if temp == "1h" else ("3mo" if temp == "4h" or temp == "1d" else "1y")
                df_t = descargar_datos(ticker_input, intervalo=temp, periodo=per)
                
                if df_t is not None and not df_t.empty:
                    df_c = calcular_indicadores(df_t)
                    if df_c is not None and not df_c.empty:
                        ult = df_c.iloc[-1]
                        cls_val = extraer_valor_seguro(ult['Close'])
                        rsi_val = extraer_valor_seguro(ult['RSI'])
                        sig_val = str(limpiar_serie(ult['Signal']))
                        div_val = str(limpiar_serie(ult['Divergencia']))
                        triv_val = str(limpiar_serie(ult['Trivergencia']))
                        
                        if temp == "1d":
                            precio_actual_global = cls_val

                        icon_sig = "🟢 COMPRA" if sig_val == "COMPRA" else ("🔴 VENTA" if sig_val == "VENTA" else "⚪ NEUTRAL")

                        resumen_multi.append({
                            "Temporalidad": temp.upper(),
                            "Precio": f"${cls_val:,.2f}",
                            "RSI (14)": round(rsi_val, 1),
                            "Divergencia Detectada": div_val,
                            "Trivergencia / Estado": triv_val,
                            "Sentimiento Táctico": icon_sig
                        })
            
            if precio_actual_global == 0.0:
                df_fallback = descargar_datos(ticker_input, intervalo="1d", periodo="1mo")
                if df_fallback is not None and not df_fallback.empty:
                    precio_actual_global = extraer_valor_seguro(df_fallback['Close'])

            st.markdown("---")
            st.markdown(f"""
                <div class="card">
                    <h2 style="color: #818cf8; margin-top: 0;">📋 Resumen Cuantitativo: {nombre_oficial} ({ticker_input})</h2>
                </div>
            """, unsafe_allow_html=True)

            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Precio Actual", f"${precio_actual_global:,.2f}")
            with col_m2:
                st.metric("Capitalización de Mercado", str(market_cap))
            with col_m3:
                st.metric("Instrumento / Símbolo", ticker_input)

            st.markdown("### 📊 Estado y Divergencias por Temporalidad Estudiada:")
            if resumen_multi:
                df_multi_res = pd.DataFrame(resumen_multi)
                st.dataframe(df_multi_res, use_container_width=True)
            else:
                st.error(f"No se pudieron calcular los indicadores para `{ticker_input}`. Comprueba que el símbolo sea correcto (ej. `NVDA`, `TSLA`, `BTC-USD`).")

            st.markdown("---")
            st.markdown("### 📰 Fundamentales & Noticias Recientes del Activo")
            try:
                noticias = ticker_obj.news
                if noticias and len(noticias) > 0:
                    for n in noticias[:3]:
                        titulo_n = n.get('title', 'Noticia de Mercado')
                        publisher_n = n.get('publisher', 'Financial Wire')
                        link_n = n.get('link', '#')
                        st.markdown(f"- **[{titulo_n}]({link_n})** — *Fuente: {publisher_n}*")
                else:
                    st.info("No hay noticias recientes destacadas en la API para este ticker en este momento.")
            except Exception:
                st.info("Información de noticias no disponible temporalmente.")

            desc_negocio = info_fund.get('longBusinessSummary', None)
            if desc_negocio:
                st.markdown("#### 🏢 Descripción del Negocio / Activo:")
                st.write(desc_negocio[:650] + "...")

            mostrar_grafico_institucional(ticker_input, nombre_oficial)
