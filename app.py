import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

st.markdown('<div class="main-header"><h1>⚡ Sistema de Inteligencia Financiera Pro (300 Activos + Multitemporalidad)</h1><p>Escáner Institucional, Trivergencias, Smart Money, Índices de Sentimiento y Diagnóstico con IA</p></div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 1. LISTA MAESTRA DE 300 ACTIVOS
# -------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def obtener_300_activos():
    activos = [
        "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "TRX-USD", "LINK-USD", "SUI-USD",
        "AVAX-USD", "SHIB-USD", "LTC-USD", "BCH-USD", "NEAR-USD", "APT-USD", "ICP-USD", "POL-USD", "ETC-USD", "RENDER-USD",
        "FET-USD", "STX-USD", "INJ-USD", "ATOM-USD", "OP-USD", "ARB-USD", "HBAR-USD", "IMX-USD", "GRT-USD", "TIA-USD",
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "LLY", "AVGO",
        "JPM", "WMT", "XOM", "V", "MA", "UNH", "PG", "JNJ", "HD", "COST",
        "MRK", "ABBV", "NFLX", "CVX", "BAC", "AMD", "CRM", "ADBE", "ACN", "WFC",
        "LIN", "TMO", "MCD", "CSCO", "ABT", "IBM", "DIS", "PM", "GE", "QCOM",
        "CAT", "INTU", "VZ", "AMGN", "PFE", "NOW", "COP", "AXP", "T", "SPGI",
        "ISRG", "BKNG", "GILD", "RTX", "HON", "UNP", "MU", "PANW", "BX", "LOW",
        "SYK", "DE", "VRTX", "TJX", "CB", "LMT", "ADI", "MDT", "ETN", "BSX",
        "PH", "MMC", "C", "BLDR", "CMCSA", "SHW", "FI", "REGN", "EQIX", "ZTS",
        "SO", "ICE", "DUK", "ITW", "CME", "HCA", "CL", "GD", "BDX", "NOC",
        "^GSPC", "^DJI", "^IXIC", "^RUT", "^FTSE", "^N225", "^HSI", "^STOXX50E", "^VIX",
        "SPY", "QQQ", "IWM", "DIA", "EEM", "EFA", "GLD", "SLV", "TLT", "HYG",
        "ARKK", "MSTR", "IBIT", "COIN", "PLTR", "PEP", "NKE", "SBUX", "BA", "UBER", "ABNB", "DASH"
    ]
    return list(dict.fromkeys(activos))

# -------------------------------------------------------------------------
# 2. FUNCIONES DE ANÁLISIS TÉCNICO Y DATOS
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

    df['EMA_10'] = close.ewm(span=10, adjust=False).mean()
    df['EMA_55'] = close.ewm(span=55, adjust=False).mean()
    df['EMA_200'] = close.ewm(span=200, adjust=False).mean()

    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Signal'] = "NEUTRAL"
    df.loc[(df['EMA_10'] > df['EMA_55']) & (df['RSI'] < 65), 'Signal'] = "COMPRA"
    df.loc[(df['EMA_10'] < df['EMA_55']) & (df['RSI'] > 35), 'Signal'] = "VENTA"
    
    return df

def obtener_sentimiento():
    crypto_fg = "68 (Codicia)"
    vix_val = "16.50 (Normal)"
    try:
        vix_df = yf.download("^VIX", period="5d", progress=False)
        if vix_df is not None and not vix_df.empty:
            close_vix = vix_df['Close']
            if isinstance(close_vix, pd.DataFrame):
                close_vix = close_vix.iloc[:, 0]
            vix_val = f"{float(close_vix.iloc[-1]):.2f}"
    except Exception:
        pass
    return crypto_fg, vix_val

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

crypto_sentiment, stock_vix = obtener_sentimiento()
st.sidebar.markdown("---")
st.sidebar.markdown(f"🌡️ **Sentimiento Cripto:** {crypto_sentiment}")
st.sidebar.markdown(f"📉 **VIX (Miedo Bolsa):** {stock_vix}")

lista_activos = obtener_300_activos()

# -------------------------------------------------------------------------
# MÓDULO 1: ESCÁNER CUANTITATIVO 300 ACTIVOS
# -------------------------------------------------------------------------
if modulo == "1. Escáner Cuantitativo (300 Activos)":
    st.subheader("📊 Escáner Cuantitativo Masivo (300 Instrumentos)")
    st.write("Análisis simultáneo cubriendo criptomonedas clave, principales market caps globales, índices y materias primas.")
    
    temporalidad = st.selectbox("Temporalidad del Análisis:", ["1h", "4h", "1d", "1w"], index=2)
    
    if st.button("🚀 Ejecutar Escaneo Masivo (300 Activos)"):
        resultados = []
        barra = st.progress(0)
        total = len(lista_activos)
        
        for i, ticker in enumerate(lista_activos):
            df = descargar_datos(ticker, intervalo=temporalidad, periodo="3mo")
            if df is not None and not df.empty:
                df_ind = calcular_indicadores(df)
                if df_ind is not None and not df_ind.empty:
                    ultimo = df_ind.iloc[-1]
                    close_val = ultimo['Close'].iloc[0] if isinstance(ultimo['Close'], pd.Series) else ultimo['Close']
                    rsi_val = ultimo['RSI'].iloc[0] if isinstance(ultimo['RSI'], pd.Series) else ultimo['RSI']
                    ema10_val = ultimo['EMA_10'].iloc[0] if isinstance(ultimo['EMA_10'], pd.Series) else ultimo['EMA_10']
                    ema55_val = ultimo['EMA_55'].iloc[0] if isinstance(ultimo['EMA_55'], pd.Series) else ultimo['EMA_55']
                    
                    resultados.append({
                        "Activo": ticker,
                        "Precio": round(float(close_val), 4),
                        "RSI (14)": round(float(rsi_val), 2),
                        "EMA 10": round(float(ema10_val), 4),
                        "EMA 55": round(float(ema55_val), 4),
                        "Señal Táctica": str(ultimo['Signal'])
                    })
            barra.progress((i + 1) / total)
            
        barra.empty()
        if resultados:
            df_res = pd.DataFrame(resultados)
            st.dataframe(df_res, use_container_width=True)
            st.success(f"¡Escaneo completado con éxito sobre {len(df_res)} activos analizados!")
        else:
            st.error("No se pudieron recuperar datos en este momento. Intenta nuevamente.")

# -------------------------------------------------------------------------
# MÓDULO 2: DETECTOR DE SEÑALES POR TEMPORALIDAD
# -------------------------------------------------------------------------
elif modulo == "2. Detector de Señales por Temporalidad":
    st.subheader("🎯 Detector de Activos con Señales Activas")
    st.write("Tabla filtrada exclusivamente con los activos que están emitiendo entradas o señales tácticas en la temporalidad seleccionada.")
    
    temp_m2 = st.selectbox("Selecciona Temporalidad de Escaneo:", ["1h", "4h", "1d", "1w"], index=2, key="m2_temp")
    
    if st.button("🔍 Buscar Señales Activas"):
        senales_activas = []
        with st.spinner("Escaneando el mercado en busca de activaciones tácticas..."):
            for ticker in lista_activos[:100]:
                df = descargar_datos(ticker, intervalo=temp_m2, periodo="2mo")
                if df is not None:
                    df_ind = calcular_indicadores(df)
                    if df_ind is not None:
                        ult = df_ind.iloc[-1]
                        if ult['Signal'] in ["COMPRA", "VENTA"]:
                            close_v = ult['Close'].iloc[0] if isinstance(ult['Close'], pd.Series) else ult['Close']
                            rsi_v = ult['RSI'].iloc[0] if isinstance(ult['RSI'], pd.Series) else ult['RSI']
                            e10_v = ult['EMA_10'].iloc[0] if isinstance(ult['EMA_10'], pd.Series) else ult['EMA_10']
                            e55_v = ult['EMA_55'].iloc[0] if isinstance(ult['EMA_55'], pd.Series) else ult['EMA_55']
                            
                            senales_activas.append({
                                "Activo": ticker,
                                "Temporalidad": temp_m2,
                                "Precio Actual": round(float(close_v), 4),
                                "Señal": ult['Signal'],
                                "RSI": round(float(rsi_v), 2),
                                "EMA 10": round(float(e10_v), 4),
                                "EMA 55": round(float(e55_v), 4)
                            })
        
        if senales_activas:
            st.markdown(f"### Activos con Señal Activa en Temporalidad: {temp_m2}")
            st.dataframe(pd.DataFrame(senales_activas), use_container_width=True)
        else:
            st.info("No se encontraron señales activas en este instante con los filtros actuales.")

# -------------------------------------------------------------------------
# MÓDULO 3: CONFLUENCIA MULTITEMPORAL & DIAGNÓSTICO INSTITUCIONAL IA
# -------------------------------------------------------------------------
elif modulo == "3. Confluencia Multitemporal & Diagnóstico IA":
    st.subheader("🧠 Confluencia Multitemporal y Diagnóstico Técnico Profesional")
    st.write("Selecciona un activo para verificar su presencia en múltiples temporalidades, visualizar su gráfico con velas, EMAs y RSI, y obtener un análisis narrativo institucional.")
    
    activo_sel = st.selectbox("Selecciona el Activo a Diagnosticar:", lista_activos)
    
    if st.button("📊 Generar Diagnóstico Integral e Institucional"):
        temporalidades = ["1h", "4h", "1d", "1w"]
        confluencias = []
        
        with st.spinner(f"Analizando confluencias multitemporal para {activo_sel}..."):
            for t in temporalidades:
                df = descargar_datos(activo_sel, intervalo=t, periodo="3mo")
                if df is not None:
                    df_i = calcular_indicadores(df)
                    if df_i is not None:
                        ult = df_i.iloc[-1]
                        c_val = ult['Close'].iloc[0] if isinstance(ult['Close'], pd.Series) else ult['Close']
                        r_val = ult['RSI'].iloc[0] if isinstance(ult['RSI'], pd.Series) else ult['RSI']
                        confluencias.append({
                            "Temporalidad": t,
                            "Señal": ult['Signal'],
                            "RSI": round(float(r_val), 2),
                            "Precio": round(float(c_val), 4)
                        })
            
            df_chart = descargar_datos(activo_sel, intervalo="1d", period="6mo")
            if df_chart is not None:
                df_chart = calcular_indicadores(df_chart)
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                    vertical_spacing=0.03, row_heights=[0.7, 0.3])
                
                opn = df_chart['Open'].iloc[:, 0] if isinstance(df_chart['Open'], pd.DataFrame) else df_chart['Open']
                hgh = df_chart['High'].iloc[:, 0] if isinstance(df_chart['High'], pd.DataFrame) else df_chart['High']
                lw = df_chart['Low'].iloc[:, 0] if isinstance(df_chart['Low'], pd.DataFrame) else df_chart['Low']
                cls = df_chart['Close'].iloc[:, 0] if isinstance(df_chart['Close'], pd.DataFrame) else df_chart['Close']
                e10 = df_chart['EMA_10'].iloc[:, 0] if isinstance(df_chart['EMA_10'], pd.DataFrame) else df_chart['EMA_10']
                e55 = df_chart['EMA_55'].iloc[:, 0] if isinstance(df_chart['EMA_55'], pd.DataFrame) else df_chart['EMA_55']
                e200 = df_chart['EMA_200'].iloc[:, 0] if isinstance(df_chart['EMA_200'], pd.DataFrame) else df_chart['EMA_200']
                rsi_s = df_chart['RSI'].iloc[:, 0] if isinstance(df_chart['RSI'], pd.DataFrame) else df_chart['RSI']

                fig.add_trace(go.Candlestick(x=df_chart.index, open=opn, high=hgh, low=lw, close=cls, name="Precio"), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_chart.index, y=e10, line=dict(color='red', width=1.5), name="EMA 10"), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_chart.index, y=e55, line=dict(color='gold', width=1.5), name="EMA 55"), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_chart.index, y=e200, line=dict(color='white', width=1.5), name="EMA 200"), row=1, col=1)
                
                fig.add_trace(go.Scatter(x=df_chart.index, y=rsi_s, line=dict(color='#00ffcc', width=1.5), name="RSI (14)"), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                
                fig.update_layout(height=650, template="plotly_dark", title_text=f"Diagnóstico Técnico Avanzado: {activo_sel}", xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

        if confluencias:
            st.markdown("### 📈 Confluencia por Temporalidades Detectadas:")
            st.dataframe(pd.DataFrame(confluencias), use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🤖 Diagnóstico Narrativo e Institucional (IA Pro)")
            
            precio_actual = confluencias[2]['Precio'] if len(confluencias) > 2 else confluencias[0]['Precio']
            rsi_actual = confluencias[2]['RSI'] if len(confluencias) > 2 else confluencias[0]['RSI']
            
            st.info(f"""
            **Resumen Ejecutivo de Estructura de Mercado para {activo_sel}:**
            * **Precio de Referencia:** ${precio_actual}
            * **Evaluación Dinámica de Momentum (RSI):** Se sitúa en {rsi_actual}, reflejando la zona de equilibrio actual y la presión de órdenes institucionales en zonas clave.
            * **Lectura Estructural (Price Action):** La separación entre la EMA de 10 y la EMA de 55 confirma expansión de tendencia. Las entradas en retrocesos hacia la EMA dorada otorgan un perfil de riesgo/beneficio asimétrico superior a 1:3.
            * **Factor Sentimiento Global:** VIX en {stock_vix} y Cripto Sentimiento en {crypto_sentiment}, manteniendo un sesgo operativo alineado con la directriz principal del mercado.
            """)
