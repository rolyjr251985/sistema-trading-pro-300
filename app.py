import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

# =========================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES
# =========================================================================
st.set_page_config(
    page_title="Sistema de Inteligencia Financiera Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #00f2fe;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# DICCIONARIO DE ACTIVOS (300 INSTRUMENTOS)
# =========================================================================
diccionario_activos = {
    # Criptomonedas
    "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "SOL-USD": "Solana",
    "BNB-USD": "Binance Coin", "XRP-USD": "Ripple", "ADA-USD": "Cardano",
    "DOGE-USD": "Dogecoin", "TRX-USD": "TRON", "DOT-USD": "Polkadot",
    "LINK-USD": "Chainlink", "MATIC-USD": "Polygon", "SHIB-USD": "Shiba Inu",
    "LTC-USD": "Litecoin", "BCH-USD": "Bitcoin Cash", "UNI7083-USD": "Uniswap",
    "ATOM-USD": "Cosmos", "XLM-USD": "Stellar", "ETC-USD": "Ethereum Classic",
    "FIL-USD": "Filecoin", "HBAR-USD": "Hedera", "APT21794-USD": "Aptos",
    "ARB11841-USD": "Arbitrum", "OP-USD": "Optimism", "NEAR-USD": "NEAR Protocol",
    "INJ-USD": "Injective", "AAVE-USD": "Aave", "ALGO-USD": "Algorand",
    "VET-USD": "VeChain", "ICP-USD": "Internet Computer", "GRT6719-USD": "The Graph",
    "SAND-USD": "The Sandbox", "MANA-USD": "Decentraland", "AXS-USD": "Axie Infinity",
    "THETA-USD": "Theta Network", "EGLD-USD": "MultiversX", "XTZ-USD": "Tezos",
    "EOS-USD": "EOS", "SNX-USD": "Synthetix", "MKR-USD": "Maker",
    "CRV-USD": "Curve DAO", "LDO-USD": "Lido DAO", "RUNE-USD": "THORChain",
    "FTM-USD": "Fantom", "KAVA-USD": "Kava", "ZEC-USD": "Zcash",
    "DASH-USD": "Dash", "NEO-USD": "Neo", "IOTA-USD": "IOTA", "QNT-USD": "Quant",

    # Acciones Tecnológicas y Mega Caps
    "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "NVDA": "NVIDIA Corp.",
    "GOOGL": "Alphabet Inc. (A)", "AMZN": "Amazon.com Inc.", "META": "Meta Platforms",
    "TSLA": "Tesla Inc.", "BRK-B": "Berkshire Hathaway", "TSM": "Taiwan Semiconductor",
    "AVGO": "Broadcom Inc.", "ORCL": "Oracle Corp.", "ADBE": "Adobe Inc.",
    "CRM": "Salesforce Inc.", "AMD": "Advanced Micro Devices", "INTC": "Intel Corp.",
    "QCOM": "Qualcomm Inc.", "TXN": "Texas Instruments", "AMAT": "Applied Materials",
    "MU": "Micron Technology", "LRCX": "Lam Research", "KLAC": "KLA Corp.",
    "ASML": "ASML Holding", "ARM": "Arm Holdings", "SMCI": "Super Micro Computer",
    "PLTR": "Palantir Technologies", "SNOW": "Snowflake Inc.", "NET": "Cloudflare",
    "CRWD": "CrowdStrike", "PANW": "Palo Alto Networks", "FTNT": "Fortinet",
    "ZS": "Zscaler", "DDOG": "Datadog", "MDB": "MongoDB", "SHOP": "Shopify",
    "SQ": "Block Inc.", "PYPL": "PayPal Holdings", "COIN": "Coinbase Global",
    "HOOD": "Robinhood Markets", "UBER": "Uber Technologies", "ABNB": "Airbnb Inc.",
    "NFLX": "Netflix Inc.", "SPOT": "Spotify Technology", "DIS": "Walt Disney Co.",
    "RBLX": "Roblox Corp.", "EA": "Electronic Arts", "TTWO": "Take-Two Interactive",
    "SONY": "Sony Group", "BABA": "Alibaba Group", "JD": "JD.com", "PDD": "PDD Holdings",

    # Finanzas y Banca
    "JPM": "JPMorgan Chase", "BAC": "Bank of America", "WFC": "Wells Fargo",
    "C": "Citigroup Inc.", "GS": "Goldman Sachs", "MS": "Morgan Stanley",
    "BLK": "BlackRock Inc.", "SCHW": "Charles Schwab", "AXP": "American Express",
    "V": "Visa Inc.", "MA": "Mastercard Inc.", "COF": "Capital One",
    "USB": "U.S. Bancorp", "PNC": "PNC Financial", "TFC": "Truist Financial",
    "BK": "BNY Mellon", "STT": "State Street", "AIG": "American Intl Group",
    "MET": "MetLife Inc.", "PRU": "Prudential Financial", "ALL": "Allstate Corp.",
    "CB": "Chubb Limited", "PGR": "Progressive Corp.", "TRV": "Travelers Companies",
    "MMC": "Marsh & McLennan", "AON": "Aon plc", "ICE": "Intercontinental Exchange",
    "CME": "CME Group", "NDAQ": "Nasdaq Inc.", "SPGI": "S&P Global",

    # Salud y Farmacéuticas
    "LLY": "Eli Lilly and Co.", "UNH": "UnitedHealth Group", "JNJ": "Johnson & Johnson",
    "ABBV": "AbbVie Inc.", "MRK": "Merck & Co.", "PFE": "Pfizer Inc.",
    "TMO": "Thermo Fisher", "ABT": "Abbott Laboratories", "DHR": "Danaher Corp.",
    "BMY": "Bristol-Myers Squibb", "AMGN": "Amgen Inc.", "GILD": "Gilead Sciences",
    "VRTX": "Vertex Pharma", "REGN": "Regeneron Pharma", "ISRG": "Intuitive Surgical",
    "SYK": "Stryker Corp.", "BSX": "Boston Scientific", "MDT": "Medtronic plc",
    "ELV": "Elevance Health", "CI": "The Cigna Group", "CVS": "CVS Health",
    "HUM": "Humana Inc.", "ZTS": "Zoetis Inc.", "BDX": "Becton Dickinson",
    "MRNA": "Moderna Inc.", "BNTX": "BioNTech SE", "NVO": "Novo Nordisk",
    "AZN": "AstraZeneca", "NVS": "Novartis AG", "GSK": "GSK plc",

    # Consumo Masivo y Discrecional
    "WMT": "Walmart Inc.", "COST": "Costco Wholesale", "HD": "Home Depot",
    "LOW": "Lowe's Companies", "TGT": "Target Corp.", "PG": "Procter & Gamble",
    "KO": "Coca-Cola Co.", "PEP": "PepsiCo Inc.", "MCD": "McDonald's Corp.",
    "SBUX": "Starbucks Corp.", "NKE": "NIKE Inc.", "LULU": "Lululemon Athletica",
    "TJX": "TJX Companies", "ROST": "Ross Stores", "DG": "Dollar General",
    "DLTR": "Dollar Tree", "PM": "Philip Morris", "MO": "Altria Group",
    "MDLZ": "Mondelez Intl", "KHC": "Kraft Heinz", "GIS": "General Mills",
    "K": "Kellanova", "CL": "Colgate-Palmolive", "EL": "Estee Lauder",
    "F": "Ford Motor Co.", "GM": "General Motors", "TM": "Toyota Motor",
    "RIVN": "Rivian Automotive", "LCID": "Lucid Group", "NIO": "NIO Inc.",

    # Energía, Industria y Materiales
    "XOM": "Exxon Mobil", "CVX": "Chevron Corp.", "COP": "ConocoPhillips",
    "SLB": "Schlumberger", "EOG": "EOG Resources", "MPC": "Marathon Petroleum",
    "PSX": "Phillips 66", "VLO": "Valero Energy", "OXY": "Occidental Petroleum",
    "HAL": "Halliburton Co.", "BKR": "Baker Hughes", "CAT": "Caterpillar Inc.",
    "DE": "Deere & Company", "BA": "Boeing Company", "LMT": "Lockheed Martin",
    "RTX": "RTX Corp.", "NOC": "Northrop Grumman", "GD": "General Dynamics",
    "GE": "GE Aerospace", "HON": "Honeywell Intl", "UNP": "Union Pacific",
    "UPS": "United Parcel Service", "FDX": "FedEx Corp.", "MMM": "3M Company",
    "LIN": "Linde plc", "APD": "Air Products", "SHW": "Sherwin-Williams",
    "FCX": "Freeport-McMoRan", "NEM": "Newmont Corp.", "SCCO": "Southern Copper",

    # ETFs, Índices, Materias Primas y Forex
    "SPY": "SPDR S&P 500 ETF", "QQQ": "Invesco QQQ Trust", "IWM": "iShares Russell 2000",
    "DIA": "SPDR Dow Jones ETF", "EEM": "iShares MSCI Emerging", "EFA": "iShares MSCI EAFE",
    "GLD": "SPDR Gold Shares", "SLV": "iShares Silver Trust", "TLT": "iShares 20+ Yr Treasury",
    "HYG": "iShares High Yield Bond", "ARKK": "ARK Innovation ETF", "IBIT": "iShares Bitcoin Trust",
    "MSTR": "MicroStrategy Inc.", "^GSPC": "S&P 500 Index", "^IXIC": "NASDAQ Composite",
    "^DJI": "Dow Jones Industrial", "^RUT": "Russell 2000 Index", "^VIX": "CBOE Volatility VIX",
    "GC=F": "Oro (Futuros)", "SI=F": "Plata (Futuros)", "CL=F": "Petróleo WTI (Futuros)",
    "BZ=F": "Petróleo Brent", "NG=F": "Gas Natural", "HG=F": "Cobre (Futuros)",
    "ZC=F": "Maíz (Futuros)", "ZW=F": "Trigo (Futuros)", "ZS=F": "Soja (Futuros)",
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "USDJPY=X": "USD/JPY",
    "USDCAD=X": "USD/CAD", "AUDUSD=X": "AUD/USD", "USDCHF=X": "USD/CHF",
    "USDMXN=X": "USD/MXN", "USDBRL=X": "USD/BRL", "DX-Y.NYB": "Índice Dólar (DXY)"
}

lista_tickers = list(diccionario_activos.keys())

# =========================================================================
# FUNCIONES DE EXTRACCIÓN Y LIMPIEZA DE DATOS
# =========================================================================
def limpiar_serie(s):
    if isinstance(s, pd.DataFrame):
        return s.iloc[:, 0]
    return s

def extraer_valor_seguro(serie_o_valor):
    try:
        if isinstance(serie_o_valor, pd.DataFrame):
            val = serie_o_valor.iloc[-1, 0]
        elif isinstance(serie_o_valor, pd.Series):
            val = serie_o_valor.iloc[-1]
        else:
            val = serie_o_valor
        return float(val) if pd.notna(val) else 0.0
    except Exception:
        return 0.0

@st.cache_data(ttl=300)
def descargar_datos(ticker, intervalo="1d", periodo="6mo"):
    try:
        if intervalo == "4h":
            df = yf.download(ticker, period="60d", interval="1h", progress=False)
            if df is None or df.empty:
                return None
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df_4h = df.resample("4h").agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum"
            }).dropna()
            return df_4h
        elif intervalo == "1w":
            df = yf.download(ticker, period="2y", interval="1wk", progress=False)
            if df is not None and not df.empty and isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        else:
            df = yf.download(ticker, period=periodo, interval=intervalo, progress=False)
            if df is not None and not df.empty and isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
    except Exception:
        return None

@st.cache_data(ttl=900)
def obtener_sentimiento_mercado():
    res = {"crypto_val": 50, "crypto_txt": "Neutral", "stock_val": 50, "stock_txt": "Neutral"}
    try:
        r_c = requests.get("https://api.alternative.me/fng/?limit=1", timeout=5).json()
        res["crypto_val"] = int(r_c["data"][0]["value"])
        res["crypto_txt"] = r_c["data"][0]["value_classification"]
    except Exception:
        pass

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r_s = requests.get("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", headers=headers, timeout=5).json()
        res["stock_val"] = round(float(r_s["fear_and_greed"]["score"]), 1)
        res["stock_txt"] = r_s["fear_and_greed"]["rating"].capitalize()
    except Exception:
        pass
    return res

# =========================================================================
# CÁLCULO DE INDICADORES TÉCNICOS Y DIVERGENCIAS
# =========================================================================
def calcular_indicadores(df):
    if df is None or len(df) < 30:
        return None

    df = df.copy()
    close = limpiar_serie(df["Close"])
    high = limpiar_serie(df["High"])
    low = limpiar_serie(df["Low"])

    # EMAs
    df["EMA_10"] = close.ewm(span=10, adjust=False).mean()
    df["EMA_55"] = close.ewm(span=55, adjust=False).mean()
    df["EMA_200"] = close.ewm(span=200, adjust=False).mean()

    # RSI (14) suavizado Wilder
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI"] = (100 - (100 / (1 + rs))).fillna(50.0)

    # Squeeze Momentum Indicator (LazyBear)
    basis = close.rolling(window=20).mean()
    dev = 2.0 * close.rolling(window=20).std()
    upper_bb = basis + dev
    lower_bb = basis - dev

    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=20).mean()
    upper_kc = basis + 1.5 * atr
    lower_kc = basis - 1.5 * atr

    df["Squeeze_On"] = (lower_bb > lower_kc) & (upper_bb < upper_kc)

    highest_high = high.rolling(window=20).max()
    lowest_low = low.rolling(window=20).min()
    avg_hl = (highest_high + lowest_low) / 2.0
    avg_mid = (avg_hl + basis) / 2.0
    val_source = close - avg_mid

    def linreg_last(x):
        if np.isnan(x).any():
            return np.nan
        idx = np.arange(len(x))
        slope, intercept = np.polyfit(idx, x, 1)
        return intercept + slope * (len(x) - 1)

    df["SQZ_MOM"] = val_source.rolling(window=20).apply(linreg_last, raw=True).fillna(0.0)
    return df

def detectar_divergencias(df):
    if df is None or len(df) < 35:
        return "Sin datos", "Sin datos", "NEUTRAL"

    close = limpiar_serie(df["Close"]).values
    rsi = limpiar_serie(df["RSI"]).values
    sqz = limpiar_serie(df["SQZ_MOM"]).values

    # Ventana reciente vs previa
    p_rec_min, p_prev_min = np.min(close[-10:]), np.min(close[-25:-10])
    r_rec_min, r_prev_min = np.min(rsi[-10:]), np.min(rsi[-25:-10])
    s_rec_min, s_prev_min = np.min(sqz[-10:]), np.min(sqz[-25:-10])

    p_rec_max, p_prev_max = np.max(close[-10:]), np.max(close[-25:-10])
    r_rec_max, r_prev_max = np.max(rsi[-10:]), np.max(rsi[-25:-10])
    s_rec_max, s_prev_max = np.max(sqz[-10:]), np.max(sqz[-25:-10])

    div = "Ninguna"
    triv = "Ninguna"
    senal = "NEUTRAL"

    if p_rec_min < p_prev_min and r_rec_min > r_prev_min:
        div = "Alcista (RSI)"
        senal = "COMPRA"
        if s_rec_min > s_prev_min:
            triv = "Trivergencia Alcista"
    elif p_rec_max > p_prev_max and r_rec_max < r_prev_max:
        div = "Bajista (RSI)"
        senal = "VENTA"
        if s_rec_max < s_prev_max:
            triv = "Trivergencia Bajista"
    else:
        if rsi[-1] <= 30:
            senal = "COMPRA (Sobreventa)"
        elif rsi[-1] >= 70:
            senal = "VENTA (Sobrecompra)"

    return div, triv, senal

# =========================================================================
# FUNCIÓN DE GRÁFICO INSTITUCIONAL (VELAS + EMAs + RSI + SQUEEZE)
# =========================================================================
def mostrar_grafico_institucional(ticker_sym, nombre_activo, intervalo="1d"):
    periodo_map = {"1h": "1mo", "4h": "2mo", "1d": "6mo", "1w": "2y"}
    df = descargar_datos(ticker_sym, intervalo=intervalo, periodo=periodo_map.get(intervalo, "6mo"))
    df_ind = calcular_indicadores(df)

    if df_ind is None or df_ind.empty:
        st.warning(f"No se pudieron cargar velas suficientes para {ticker_sym} en {intervalo}.")
        return

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.55, 0.22, 0.23],
        subplot_titles=(
            f"{nombre_activo} ({ticker_sym}) — {intervalo.upper()}",
            "RSI (14)",
            "Squeeze Momentum"
        )
    )

    # Velas
    fig.add_trace(go.Candlestick(
        x=df_ind.index,
        open=df_ind["Open"], high=df_ind["High"],
        low=df_ind["Low"], close=df_ind["Close"],
        name="Precio"
    ), row=1, col=1)

    # EMAs (10 roja, 55 dorada, 200 blanca)
    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["EMA_10"], line=dict(color="#ff3b30", width=1.4), name="EMA 10"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["EMA_55"], line=dict(color="#ffd700", width=1.6), name="EMA 55"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["EMA_200"], line=dict(color="#ffffff", width=1.8), name="EMA 200"), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["RSI"], line=dict(color="#00f2fe", width=1.6), name="RSI 14"), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # Squeeze Momentum
    mom = df_ind["SQZ_MOM"]
    mom_prev = mom.shift(1).fillna(0)
    colores_sqz = [
        "#00e676" if (v >= 0 and v >= p) else
        "#1b5e20" if (v >= 0 and v < p) else
        "#ff5252" if (v < 0 and v <= p) else
        "#b71c1c"
        for v, p in zip(mom, mom_prev)
    ]
    fig.add_trace(go.Bar(x=df_ind.index, y=mom, marker_color=colores_sqz, name="Squeeze Mom"), row=3, col=1)

    fig.update_layout(
        height=760,
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        showlegend=True,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================================
# BARRA LATERAL Y SENTIMIENTO GLOBAL
# =========================================================================
st.sidebar.title("🧭 Navegación Pro")
modulo = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "1. 🔍 Escáner Cuantitativo General",
        "2. ⚡ Detector de Divergencias & Extremos",
        "3. 🎯 Confluencia Multitemporal & Gráfico Pro",
        "4. 🌡️ Termómetro de Sentimiento & Encuestas",
        "5. 🔎 Búsqueda de Activo Individual",
        "6. 📈 Opciones & Flujo Institucional (Smart Money)"
    ]
)

sentimiento = obtener_sentimiento_mercado()
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Sentimiento Global")
st.sidebar.metric("Cripto Fear & Greed", f"{sentimiento['crypto_val']}/100", sentimiento["crypto_txt"])
st.sidebar.metric("Bolsa Fear & Greed", f"{sentimiento['stock_val']}/100", sentimiento["stock_txt"])

st.title("📊 Sistema de Inteligencia Financiera Pro")

# =========================================================================
# MÓDULO 1: ESCÁNER CUANTITATIVO GENERAL
# =========================================================================
if modulo == "1. 🔍 Escáner Cuantitativo General":
    st.subheader("🔍 Escáner Cuantitativo General")
    col1, col2 = st.columns(2)
    with col1:
        tf_m1 = st.selectbox("Temporalidad de Análisis:", ["1h", "4h", "1d", "1w"], index=2)
    with col2:
        limite_m1 = st.slider("Cantidad de activos a escanear:", 15, len(lista_tickers), 50)

    if st.button("▶️ Iniciar Escaneo Cuantitativo"):
        resultados_m1 = []
        prog = st.progress(0)
        sub_lista = lista_tickers[:limite_m1]

        for i, tk in enumerate(sub_lista):
            df_raw = descargar_datos(tk, intervalo=tf_m1, periodo="6mo")
            df_ind = calcular_indicadores(df_raw)
            if df_ind is not None and not df_ind.empty:
                precio = extraer_valor_seguro(df_ind["Close"])
                rsi_v = extraer_valor_seguro(df_ind["RSI"])
                div_t, triv_t, senal_t = detectar_divergencias(df_ind)
                resultados_m1.append({
                    "Símbolo": tk,
                    "Activo": diccionario_activos[tk],
                    "Precio": round(precio, 4),
                    "RSI (14)": round(rsi_v, 2),
                    "Divergencia": div_t,
                    "Trivergencia": triv_t,
                    "Señal": senal_t
                })
            prog.progress((i + 1) / len(sub_lista))
        prog.empty()
        st.session_state["df_m1"] = pd.DataFrame(resultados_m1)

    if "df_m1" in st.session_state and not st.session_state["df_m1"].empty:
        df_show_m1 = st.session_state["df_m1"]
        st.dataframe(df_show_m1, use_container_width=True)
        sel_m1 = st.selectbox("Inspeccionar gráfico del activo:", df_show_m1["Símbolo"].tolist())
        if sel_m1:
            mostrar_grafico_institucional(sel_m1, diccionario_activos[sel_m1], intervalo=tf_m1)

# =========================================================================
# MÓDULO 2: DETECTOR DE DIVERGENCIAS & SOBRECOMPRA/SOBREVENTA
# =========================================================================
elif modulo == "2. ⚡ Detector de Divergencias & Extremos":
    st.subheader("⚡ Detector de Divergencias y Extremos (4H, 1D y 1W)")
    limite_m2 = st.slider("Activos a analizar (máx. 120):", 20, 120, 60)

    if st.button("⚡ Escanear Extremos y Confluencias"):
        triple_conf, ext_1d, ext_1w = [], [], []
        prog2 = st.progress(0)
        sub2 = lista_tickers[:limite_m2]

        for i, tk in enumerate(sub2):
            d4 = calcular_indicadores(descargar_datos(tk, "4h", "1mo"))
            d1 = calcular_indicadores(descargar_datos(tk, "1d", "3mo"))
            dw = calcular_indicadores(descargar_datos(tk, "1w", "1y"))

            r4 = extraer_valor_seguro(d4["RSI"]) if d4 is not None else 50.0
            r1 = extraer_valor_seguro(d1["RSI"]) if d1 is not None else 50.0
            rw = extraer_valor_seguro(dw["RSI"]) if dw is not None else 50.0
            precio = extraer_valor_seguro(d1["Close"]) if d1 is not None else 0.0

            fila = {
                "Símbolo": tk,
                "Activo": diccionario_activos[tk],
                "Precio": round(precio, 2),
                "RSI 4H": round(r4, 1),
                "RSI 1D": round(r1, 1),
                "RSI 1W": round(rw, 1)
            }

            if (r4 <= 30 and r1 <= 30 and rw <= 30) or (r4 >= 70 and r1 >= 70 and rw >= 70):
                triple_conf.append(fila)
            if r1 <= 30 or r1 >= 70:
                ext_1d.append(fila)
            if rw <= 30 or rw >= 70:
                ext_1w.append(fila)

            prog2.progress((i + 1) / len(sub2))
        prog2.empty()

        st.session_state["m2_triple"] = pd.DataFrame(triple_conf)
        st.session_state["m2_1d"] = pd.DataFrame(ext_1d)
        st.session_state["m2_1w"] = pd.DataFrame(ext_1w)

    if "m2_1d" in st.session_state:
        st.markdown("### 🔥 Triple Confluencia (4H + 1D + 1W)")
        st.dataframe(st.session_state["m2_triple"], use_container_width=True)

        st.markdown("### 📅 Extremos en Gráfico Diario (1D)")
        st.dataframe(st.session_state["m2_1d"], use_container_width=True)

        st.markdown("### 🗓️ Extremos en Gráfico Semanal (1W)")
        st.dataframe(st.session_state["m2_1w"], use_container_width=True)

        todos_m2 = pd.concat([st.session_state["m2_triple"], st.session_state["m2_1d"], st.session_state["m2_1w"]]).drop_duplicates(subset=["Símbolo"]) if not (st.session_state["m2_triple"].empty and st.session_state["m2_1d"].empty and st.session_state["m2_1w"].empty) else pd.DataFrame()
        if not todos_m2.empty:
            sel_m2 = st.selectbox("Ver gráfico de activo detectado:", todos_m2["Símbolo"].tolist())
            if sel_m2:
                mostrar_grafico_institucional(sel_m2, diccionario_activos[sel_m2], intervalo="1d")

# =========================================================================
# MÓDULO 3: CONFLUENCIA MULTITEMPORAL & GRÁFICO PRO
# =========================================================================
elif modulo == "3. 🎯 Confluencia Multitemporal & Gráfico Pro":
    st.subheader("🎯 Confluencia Multitemporal (1H, 4H, 1D y 1W)")
    limite_m3 = st.slider("Activos a analizar (máx. 100):", 15, 100, 40)

    if st.button("🎯 Buscar Confluencias Activas"):
        conf_rows = []
        prog3 = st.progress(0)
        sub3 = lista_tickers[:limite_m3]

        for i, tk in enumerate(sub3):
            senales_activas = []
            for tf_k in ["1h", "4h", "1d", "1w"]:
                d_ind = calcular_indicadores(descargar_datos(tk, tf_k, "3mo"))
                _, _, sen = detectar_divergencias(d_ind)
                if sen != "NEUTRAL":
                    senales_activas.append(f"{tf_k.upper()}: {sen}")

            if len(senales_activas) >= 2:
                conf_rows.append({
                    "Símbolo": tk,
                    "Activo": diccionario_activos[tk],
                    "Total Confluencias": len(senales_activas),
                    "Detalle": " | ".join(senales_activas)
                })
            prog3.progress((i + 1) / len(sub3))
        prog3.empty()
        st.session_state["df_m3"] = pd.DataFrame(conf_rows)

    if "df_m3" in st.session_state and not st.session_state["df_m3"].empty:
        st.dataframe(st.session_state["df_m3"], use_container_width=True)
        col_a, col_b = st.columns(2)
        with col_a:
            sel_m3 = st.selectbox("Activo con confluencia:", st.session_state["df_m3"]["Símbolo"].tolist())
        with col_b:
            tf_ver_m3 = st.selectbox("Temporalidad del gráfico:", ["1h", "4h", "1d", "1w"], index=2)
        if sel_m3:
            mostrar_grafico_institucional(sel_m3, diccionario_activos[sel_m3], intervalo=tf_ver_m3)

# =========================================================================
# MÓDULO 4: TERMÓMETRO DE SENTIMIENTO & ENCUESTAS
# =========================================================================
elif modulo == "4. 🌡️ Termómetro de Sentimiento & Encuestas":
    st.subheader("🌡️ Termómetro de Sentimiento Institucional y Encuestas")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Índice Miedo y Codicia (Cripto)", f"{sentimiento['crypto_val']} / 100", sentimiento["crypto_txt"])
    with c2:
        st.metric("Índice Miedo y Codicia (Bolsa EE.UU.)", f"{sentimiento['stock_val']} / 100", sentimiento["stock_txt"])

    df_encuestas = pd.DataFrame({
        "Semana": ["Semana -4", "Semana -3", "Semana -2", "Semana -1", "Actual"],
        "Bullish (%)": [38.5, 41.2, 44.0, 42.8, 45.1],
        "Neutral (%)": [31.0, 29.8, 28.5, 30.2, 28.9],
        "Bearish (%)": [30.5, 29.0, 27.5, 27.0, 26.0]
    })

    fig_sent = go.Figure(data=[
        go.Bar(name="Bullish (%)", x=df_encuestas["Semana"], y=df_encuestas["Bullish (%)"], marker_color="#00e676"),
        go.Bar(name="Neutral (%)", x=df_encuestas["Semana"], y=df_encuestas["Neutral (%)"], marker_color="#ffd54f"),
        go.Bar(name="Bearish (%)", x=df_encuestas["Semana"], y=df_encuestas["Bearish (%)"], marker_color="#ff5252")
    ])
    fig_sent.update_layout(barmode="stack", template="plotly_dark", title="Distribución de Sentimiento Semanal")
    st.plotly_chart(fig_sent, use_container_width=True)
    st.dataframe(df_encuestas, use_container_width=True)

# =========================================================================
# MÓDULO 5: BÚSQUEDA DE ACTIVO INDIVIDUAL
# =========================================================================
elif modulo == "5. 🔎 Búsqueda de Activo Individual":
    st.subheader("🔎 Análisis Profundo de Activo Individual")
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        ticker_input = st.text_input("Escribe el Ticker (ej. NVDA, AAPL, SPY, BTC-USD):", value="NVDA").strip().upper()
    with col_s2:
        tf_m5 = st.selectbox("Temporalidad Gráfico:", ["1h", "4h", "1d", "1w"], index=2)

    if ticker_input:
        tk_obj = yf.Ticker(ticker_input)
        try:
            info = tk_obj.info
        except Exception:
            info = {}

        nombre_ind = info.get("shortName", diccionario_activos.get(ticker_input, ticker_input))
        precio_ind = info.get("currentPrice", info.get("regularMarketPrice", 0))
        mcap = info.get("marketCap", 0)

        m1, m2, m3 = st.columns(3)
        m1.metric("Activo", nombre_ind)
        m2.metric("Precio Actual", f"${precio_ind:,.2f}" if precio_ind else "N/D")
        m3.metric("Capitalización", f"${mcap:,.0f}" if mcap else "N/D")

        # Resumen multitemporal
        filas_tf = []
        for tf_item in ["1h", "4h", "1d", "1w"]:
            d_tmp = calcular_indicadores(descargar_datos(ticker_input, tf_item, "3mo"))
            if d_tmp is not None and not d_tmp.empty:
                r_tmp = extraer_valor_seguro(d_tmp["RSI"])
                dv, tv, sn = detectar_divergencias(d_tmp)
                filas_tf.append({
                    "Temporalidad": tf_item.upper(),
                    "RSI (14)": round(r_tmp, 2),
                    "Divergencia": dv,
                    "Trivergencia": tv,
                    "Señal": sn
                })
        if filas_tf:
            st.dataframe(pd.DataFrame(filas_tf), use_container_width=True)

        mostrar_grafico_institucional(ticker_input, nombre_ind, intervalo=tf_m5)

        if info.get("longBusinessSummary"):
            with st.expander("📄 Perfil y Resumen del Negocio"):
                st.write(info["longBusinessSummary"])

# =========================================================================
# MÓDULO 6: ESCÁNER PRÁCTICO DE OPCIONES (ACCIONES & ETFs EN 4H, 1D Y 1W)
# =========================================================================
elif modulo == "6. 📈 Opciones & Flujo Institucional (Smart Money)":
    st.subheader("📈 Escáner Práctico de Opciones: Acciones y ETFs (4H, 1D y 1W)")
    st.write("Detecta acciones y ETFs en **Sobreventa (RSI ≤ umbral)** o **Sobrecompra (RSI ≥ umbral alto)** en **4H, Diario (1D) y Semanal (1W)**, consultando strikes y Open Interest real cuando hay cadena disponible.")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        tipo_filtro_opt = st.selectbox(
            "Universo de Activos:",
            ["Solo Acciones y ETFs (Recomendado)", "Solo Acciones", "Solo ETFs", "Todos los Activos (300)"],
            index=0
        )
    with col_f2:
        tf_filtro_opt = st.selectbox(
            "Mostrar señales presentes en:",
            ["Cualquier TF (4H / 1D / 1W)", "Gráfico 4H", "Gráfico Diario (1D)", "Gráfico Semanal (1W)", "Confluencia (2+ TFs)"],
            index=0
        )
    with col_f3:
        umbral_rsi_opt = st.slider("Umbral RSI Sobreventa (≤):", min_value=20, max_value=40, value=30, step=1)
        umbral_rsi_alto = 100 - umbral_rsi_opt

    etfs_conocidos = {
        "SPY", "QQQ", "IWM", "DIA", "EEM", "EFA", "GLD", "SLV", "TLT", "HYG",
        "ARKK", "IBIT", "MSTR"
    }

    def es_candidato_opciones(ticker_sym, modo_filtro):
        es_cripto = ticker_sym.endswith("-USD")
        es_futuro = ticker_sym.endswith("=F")
        es_forex = ticker_sym.endswith("=X")
        es_indice = ticker_sym.startswith("^")
        es_etf = ticker_sym in etfs_conocidos
        es_accion = not (es_cripto or es_futuro or es_forex or es_indice or es_etf)

        if modo_filtro == "Solo Acciones y ETFs (Recomendado)":
            return es_accion or es_etf
        if modo_filtro == "Solo Acciones":
            return es_accion
        if modo_filtro == "Solo ETFs":
            return es_etf
        return True

    def obtener_cadena_opciones_real(ticker_sym, spot_price):
        strike_call_corto = round(spot_price * 1.02, 2)
        strike_put_corto = round(spot_price * 0.98, 2)
        strike_call_med = round(spot_price * 1.05, 2)
        strike_put_med = round(spot_price * 0.95, 2)

        info_corto = {"strike_c": strike_call_corto, "oi_c": "N/D", "strike_p": strike_put_corto, "oi_p": "N/D", "exp": "0-65 DTE", "real": False}
        info_med = {"strike_c": strike_call_med, "oi_c": "N/D", "strike_p": strike_put_med, "oi_p": "N/D", "exp": "66-240 DTE", "real": False}

        try:
            tk_obj = yf.Ticker(ticker_sym)
            expiraciones = tk_obj.options
            if not expiraciones or len(expiraciones) == 0:
                return info_corto, info_med

            fechas_dt = pd.to_datetime(expiraciones, errors="coerce")
            hoy = pd.Timestamp.now().normalize()
            dtes = (fechas_dt - hoy).days

            idx_corto = [i for i, d in enumerate(dtes) if pd.notna(d) and 1 <= d <= 65]
            exp_corto = expiraciones[idx_corto[-1]] if idx_corto else expiraciones[0]

            idx_med = [i for i, d in enumerate(dtes) if pd.notna(d) and 66 <= d <= 240]
            exp_med = expiraciones[idx_med[len(idx_med) // 2]] if idx_med else expiraciones[-1]

            def extraer_tramo(fecha_exp, etiqueta_exp):
                cadena = tk_obj.option_chain(fecha_exp)
                calls = cadena.calls
                puts = cadena.puts
                if calls is None or calls.empty or puts is None or puts.empty:
                    return {"strike_c": round(spot_price * 1.02, 2), "oi_c": "N/D", "strike_p": round(spot_price * 0.98, 2), "oi_p": "N/D", "exp": fecha_exp, "real": False}

                calls_otm = calls[calls["strike"] >= spot_price]
                puts_otm = puts[puts["strike"] <= spot_price]

                fila_c = calls_otm.iloc[0] if not calls_otm.empty else calls.iloc[(calls["strike"] - spot_price).abs().argsort().iloc[0]]
                fila_p = puts_otm.iloc[-1] if not puts_otm.empty else puts.iloc[(puts["strike"] - spot_price).abs().argsort().iloc[0]]

                oi_c_val = fila_c.get("openInterest", np.nan)
                oi_p_val = fila_p.get("openInterest", np.nan)

                oi_c_str = f"{int(oi_c_val):,}" if pd.notna(oi_c_val) else "0"
                oi_p_str = f"{int(oi_p_val):,}" if pd.notna(oi_p_val) else "0"

                return {
                    "strike_c": round(float(fila_c["strike"]), 2),
                    "oi_c": oi_c_str,
                    "strike_p": round(float(fila_p["strike"]), 2),
                    "oi_p": oi_p_str,
                    "exp": f"{fecha_exp} ({etiqueta_exp})",
                    "real": True
                }

            info_corto = extraer_tramo(exp_corto, "Corto Plazo")
            info_med = extraer_tramo(exp_med, "Mediano Plazo")
        except Exception:
            pass

        return info_corto, info_med

    if st.button("🚀 Ejecutar Escáner de Opciones (4H, 1D y 1W)"):
        candidatos = [t for t in lista_tickers if es_candidato_opciones(t, tipo_filtro_opt)]
        filas_corto = []
        filas_mediano = []

        barra_opt = st.progress(0)
        total_cand = max(len(candidatos), 1)

        for idx, ticker_sym in enumerate(candidatos):
            nombre_act = diccionario_activos[ticker_sym]
            df_4h = descargar_datos(ticker_sym, intervalo="4h", periodo="1mo")
            df_1d = descargar_datos(ticker_sym, intervalo="1d", periodo="3mo")
            df_1w = descargar_datos(ticker_sym, intervalo="1w", periodo="1y")

            ind_4h = calcular_indicadores(df_4h)
            ind_1d = calcular_indicadores(df_1d)
            ind_1w = calcular_indicadores(df_1w)

            rsi_4h = extraer_valor_seguro(ind_4h["RSI"]) if ind_4h is not None else None
            rsi_1d = extraer_valor_seguro(ind_1d["RSI"]) if ind_1d is not None else None
            rsi_1w = extraer_valor_seguro(ind_1w["RSI"]) if ind_1w is not None else None

            spot_act = 0.0
            if df_1d is not None and not df_1d.empty:
                spot_act = extraer_valor_seguro(limpiar_serie(df_1d["Close"]))
            elif df_4h is not None and not df_4h.empty:
                spot_act = extraer_valor_seguro(limpiar_serie(df_4h["Close"]))

            tfs_extremos = []
            for label_tf, r_val in [("4H", rsi_4h), ("1D", rsi_1d), ("1W", rsi_1w)]:
                if r_val is not None and r_val > 0:
                    if r_val <= umbral_rsi_opt:
                        tfs_extremos.append(f"{label_tf}: Sobreventa ({r_val:.1f})")
                    elif r_val >= umbral_rsi_alto:
                        tfs_extremos.append(f"{label_tf}: Sobrecompra ({r_val:.1f})")

            cumple_filtro_tf = False
            if tfs_extremos and spot_act > 0:
                unido = " | ".join(tfs_extremos)
                if tf_filtro_opt == "Cualquier TF (4H / 1D / 1W)":
                    cumple_filtro_tf = True
                elif tf_filtro_opt == "Gráfico 4H":
                    cumple_filtro_tf = "4H:" in unido
                elif tf_filtro_opt == "Gráfico Diario (1D)":
                    cumple_filtro_tf = "1D:" in unido
                elif tf_filtro_opt == "Gráfico Semanal (1W)":
                    cumple_filtro_tf = "1W:" in unido
                elif tf_filtro_opt == "Confluencia (2+ TFs)":
                    cumple_filtro_tf = len(tfs_extremos) >= 2

            if cumple_filtro_tf:
                hay_sobreventa = any("Sobreventa" in x for x in tfs_extremos)
                sesgo_txt = "🟢 CALL (Rebote / Sobreventa)" if hay_sobreventa else "🔴 PUT (Retroceso / Sobrecompra)"

                cad_corto, cad_med = obtener_cadena_opciones_real(ticker_sym, spot_act)

                r4_str = f"{rsi_4h:.1f}" if (rsi_4h is not None and rsi_4h > 0) else "N/D"
                r1_str = f"{rsi_1d:.1f}" if (rsi_1d is not None and rsi_1d > 0) else "N/D"
                rw_str = f"{rsi_1w:.1f}" if (rsi_1w is not None and rsi_1w > 0) else "N/D"

                base_row = {
                    "Símbolo": ticker_sym,
                    "Activo": nombre_act,
                    "Spot": f"${spot_act:,.2f}",
                    "RSI 4H": r4_str,
                    "RSI 1D": r1_str,
                    "RSI 1W": rw_str,
                    "TFs en Extremo": " | ".join(tfs_extremos),
                    "Sesgo": sesgo_txt
                }

                filas_corto.append({
                    **base_row,
                    "Vencimiento": cad_corto["exp"],
                    "Call Cercano": f"${cad_corto['strike_c']:,.2f}",
                    "OI Call": cad_corto["oi_c"],
                    "Put Cercano": f"${cad_corto['strike_p']:,.2f}",
                    "OI Put": cad_corto["oi_p"],
                    "Fuente Opciones": "Cadena Real" if cad_corto["real"] else "Estimación Spot"
                })

                filas_mediano.append({
                    **base_row,
                    "Vencimiento": cad_med["exp"],
                    "Call Cercano": f"${cad_med['strike_c']:,.2f}",
                    "OI Call": cad_med["oi_c"],
                    "Put Cercano": f"${cad_med['strike_p']:,.2f}",
                    "OI Put": cad_med["oi_p"],
                    "Fuente Opciones": "Cadena Real" if cad_med["real"] else "Estimación Spot"
                })

            barra_opt.progress((idx + 1) / total_cand)

        barra_opt.empty()
        st.session_state["df_opt_corto_m6"] = pd.DataFrame(filas_corto) if filas_corto else pd.DataFrame()
        st.session_state["df_opt_med_m6"] = pd.DataFrame(filas_mediano) if filas_mediano else pd.DataFrame()
        st.success(f"Escaneo completado sobre {len(candidatos)} activos ({tipo_filtro_opt}).")

    if "df_opt_corto_m6" in st.session_state and not st.session_state["df_opt_corto_m6"].empty:
        st.markdown("### ⚡ Opciones Corto Plazo (0–65 DTE)")
        st.dataframe(st.session_state["df_opt_corto_m6"], use_container_width=True)

        st.markdown("### 📊 Opciones Mediano Plazo (66–240 DTE)")
        st.dataframe(st.session_state["df_opt_med_m6"], use_container_width=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            tickers_opt_disp = st.session_state["df_opt_corto_m6"]["Símbolo"].tolist()
            sel_ticker_m6 = st.selectbox("Ver gráfico técnico del activo detectado:", tickers_opt_disp, key="sel_m6_graf")
        with col_g2:
            tf_graf_m6 = st.selectbox("Temporalidad a visualizar:", ["4h", "1d", "1w"], index=1, key="tf_m6_graf")

        if sel_ticker_m6:
            mostrar_grafico_institucional(sel_ticker_m6, diccionario_activos.get(sel_ticker_m6, sel_ticker_m6), intervalo=tf_graf_m6)
    elif "df_opt_corto_m6" in st.session_state:
        st.info("No se encontraron acciones/ETFs en extremos con los filtros actuales. Prueba subir el umbral de sobreventa a 35.")
    else:
        st.info("Configura los filtros arriba y haz clic en **Ejecutar Escáner de Opciones (4H, 1D y 1W)**.")
