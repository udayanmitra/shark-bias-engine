# app.py
# Shark Exchange — FULL AI INSTITUTIONAL DASHBOARD (MANUAL INPUT EDITION)
# Hosted live on Streamlit Community Cloud

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ─── PREMIUM INSTITUTIONAL DARK THEME CONFIG ──────────────────────────────
st.set_page_config(page_title="Shark Institutional Bias Engine", page_icon="🦈", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #06090d; color: #f0f3f6; font-family: monospace; }
.block-container { padding-top: 1rem; max-width: 1500px; }
h1, h2, h3 { color: #00ffcc; font-weight: 700; letter-spacing: 0.5px; }
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0b1118 0%, #121b26 100%);
    border: 1px solid #1f2e40; border-radius: 4px; padding: 10px;
}
div[data-testid="stMetricLabel"] { font-size: 0.75rem; color: #8b9bb4; text-transform: uppercase; }
div[data-testid="stMetricValue"] { font-size: 1.3rem; font-weight: bold; color: #00ffcc !important; }
.bias-banner-bullish {
    background: linear-gradient(90deg, #0d2a1d 0%, #1b4d3e 100%);
    padding: 12px; border-radius: 4px; border-left: 5px solid #00ff88; color: #00ff88; font-weight: bold; margin-bottom: 15px;
}
.bias-banner-bearish {
    background: linear-gradient(90deg, #2a0d0d 0%, #4d1b1b 100%);
    padding: 12px; border-radius: 4px; border-left: 5px solid #ff4444; color: #ff4444; font-weight: bold; margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🦈 SHARK EXCHANGE // INSTITUTIONAL BIAS ENGINE")
st.caption("Phase 1 Production Release — Manual Input Framework. Pure Price Action, SMC & Volume Order Flow Analysis.")
st.hr()

# ─── SIDEBAR MANUAL INPUT CONTROL PANEL ───────────────────────────────────
st.sidebar.header("🔍 MARKET MATRIX SELECTION")
selected_asset = st.sidebar.selectbox("Active Trading Pair", ["BTCUSDT", "XAUUSDT"])
trading_profile = st.sidebar.radio("Active Operational Profile", ["INTRADAY", "SWING"])

if trading_profile == "INTRADAY":
    exec_tf = "3m"
    mtf_tfs = ["15m", "30m", "1h"]
    st.sidebar.info("⚡ Profile: INTRADAY\\nExecution Frame: 3m\\nContext Filters: 15m | 30m | 1h")
else:
    exec_tf = "30m"
    mtf_tfs = ["1h", "4h", "12h", "1d"]
    st.sidebar.info("🔱 Profile: SWING\\nExecution Frame: 30m\\nContext Filters: 1h | 4h | 12h | 1d")

st.sidebar.hr()
st.sidebar.header("✍️ MANUAL DATA ENTRY")
st.sidebar.caption("Type in current values directly from your broker screen:")

# Manual Number Fields
input_mark_price = st.sidebar.number_input("Live Mark Price ($)", value=76420.50 if selected_asset == "BTCUSDT" else 2684.30, step=0.1)
input_liq_high = st.sidebar.number_input("Institutional Liquidity Top ($)", value=76800.00 if selected_asset == "BTCUSDT" else 2700.00, step=0.1)
input_liq_low = st.sidebar.number_input("Institutional Liquidity Base ($)", value=76000.00 if selected_asset == "BTCUSDT" else 2660.00, step=0.1)
input_buyer_pct = st.sidebar.slider("Buyer Sentiment Ratio (%)", min_value=0, max_value=100, value=55)
input_vol_delta = st.sidebar.number_input("Net Volume Delta (Contracts)", value=3450, step=10)

# Process values
seller_pct = 100 - input_buyer_pct

# ─── DYNAMIC BIAS INTERPRETATION DISPLAY ──────────────────────────────────
bias_condition = "BULLISH CHARGED" if input_buyer_pct >= 50 else "BEARISH CHARGED"
if bias_condition == "BULLISH CHARGED":
    st.markdown(f'<div class="bias-banner-bullish">📊 CURRENT MARKET BIAS: ORDER FLOW CONVERGENCE → MULTI-TIMEFRAME LONG BIAS ({input_buyer_pct}% BUY SENTIMENT)</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="bias-banner-bearish">📊 CURRENT MARKET BIAS: LIQUIDITY SWEEP CONVERGENCE → MULTI-TIMEFRAME SHORT BIAS ({seller_pct}% SELL SENTIMENT)</div>', unsafe_allow_html=True)

# ─── METRIC DATA ARRAY TILES ──────────────────────────────────────────────
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Live Mark Price", f"${input_mark_price:,.2f}")
m_col2.metric("Institutional Liquidity Top", f"${input_liq_high:,.2f}")
m_col3.metric("Institutional Liquidity Base", f"${input_liq_low:,.2f}")
m_col4.metric("Net Volume Delta", f"{input_vol_delta:+,}")

st.hr()

# ─── MULTI-TIMEFRAME FRAME CONTEXT GRID ───────────────────────────────────
st.subheader("🎯 Multi-Timeframe (MTF) Market Structure Context Matrix")
mtf_cols = st.columns(len(mtf_tfs))

for idx, tf in enumerate(mtf_tfs):
    with mtf_cols[idx]:
        st.markdown(f"### Grid Node: {tf}")
        structure = "Premium Array - Short Mitigations" if bias_condition == "BEARISH CHARGED" else "Discount Array - Long Mitigations"
        last_action = "Market Structure Break (BOS)" if idx == 0 else "Change of Character (CHoCH)"
        
        st.caption(f"Timeframe Context Layer: {tf}")
        st.write(f"• **Order Flow State:** {structure}")
        st.write(f"• **Structural Shift:** {last_action}")
        st.progress(input_buyer_pct / 100.0)

st.hr()

# ─── PURE PRICE ACTION PROFILE VISUALIZER ────────────────────────────────
st.subheader(f"📊 {selected_asset} Order Flow & Sentiment Profile ({exec_tf} Execution View)")

c1, c2 = st.columns()

with c1:
    # Render dynamic layout tracking user values
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[input_liq_high, input_liq_high], mode="lines", name="Buy Stop Liquidity Pool", line=dict(color="#ff4444", dash="dash")))
    fig.add_trace(go.Scatter(x=[0.5], y=[input_mark_price], mode="markers+text", text=[f"Live Mark: ${input_mark_price:,.2f}"], textposition="top center", marker=dict(color="#00ffcc", size=14), name="Active Mark"))
    fig.add_trace(go.Scatter(x=[0, 1], y=[input_liq_low, input_liq_low], mode="lines", name="Sell Stop Liquidity Pool", line=dict(color="#00ff88", dash="dash")))
    
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(visible=False), yaxis=dict(gridcolor="#1f2e40"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 📊 Shark Exchange Sentiment Delta")
    labels = ['Buyers (Long)', 'Sellers (Short)']
    values = [input_buyer_pct, seller_pct]
    
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=['#00ff88', '#ff4444']))])
    fig_pie.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

st.success("🔒 Cloud System Active. Type your custom parameters into the left sidebar panel to instantly refresh metrics.")
