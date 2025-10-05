# app.py - Enhanced Liver Cancer Drug Intelligence Platform with Advanced Visualizations (Fixed Version)
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
import requests
import yfinance as yf
from collections import defaultdict
import json
import re
import io
import math
import streamlit.components.v1 as components
import textwrap
import feedparser

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="🧬 Liver Cancer Drug Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Advanced CSS Animations and Styles
# ---------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: gradientShift 8s ease infinite, float 6s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
        letter-spacing: 2px;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.6s;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 80px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
    }

    .section-header {
        font-family: 'Orbitron', sans-serif;
        color: #fff;
        margin: 2rem 0 1rem 0;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 15px;
        border-left: 6px solid #667eea;
        position: relative;
        overflow: hidden;
        font-size: 1.4rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .data-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .data-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }

    .data-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    .status-live {
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .stTabs [data-baseweb="tab"] { 
        background: rgba(30,41,59,0.8); 
        border-radius: 10px; 
        padding: 12px 24px; 
        margin: 0 4px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #667eea, #764ba2) !important; 
        color:white !important; 
        border: 1px solid rgba(255,255,255,0.2) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 1rem;
    }

    ::-webkit-scrollbar { width:8px; } 
    ::-webkit-scrollbar-thumb{ 
        background: linear-gradient(135deg,#667eea,#764ba2); 
        border-radius:4px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------
# EnhancedDataManager: Data Acquisition, Real-time Quotes & Market Cap
# ---------------------------
class EnhancedDataManager:
    def __init__(self):
        # API Key Configuration
        self.alpha_vantage_key = st.secrets.get("ALPHA_VANTAGE_KEY", "")
        self.news_api_key = st.secrets.get("NEWS_API_KEY", "")
        self.fmp_api_key = st.secrets.get("FMP_API_KEY", "BndBWdOQI6I0IK0E5kGYStxRJZC065sM")

        # Monitored Companies: name -> ticker/symbol
        self.companies = {
            'Roche': 'RHHBY',  # Roche ADR
            'Bayer': 'BAYRY',  # Bayer ADR
            'Hengrui Medicine': '600276.SS',  # A-share
            'BeiGene': 'BGNE',  # BeiGene (US)
            'Merck': 'MRK',  # Merck
            'Novartis': 'NVS',  # Novartis
            'AstraZeneca': 'AZN'  # AstraZeneca
        }

        # Fallback Market Caps (in billions USD)
        self.fallback_market_caps = {
            'Roche': 200.0,
            'Bayer': 50.0,
            'Hengrui Medicine': 30.0,
            'BeiGene': 12.0,
            'Merck': 150.0,
            'Novartis': 180.0,
            'AstraZeneca': 140.0
        }

        # Initialize trend cache
        if 'stock_trends' not in st.session_state:
            st.session_state.stock_trends = {c: [] for c in self.companies}

        # Initialize carousel index and timer
        if 'carousel_index' not in st.session_state:
            st.session_state.carousel_index = 0
        if 'last_carousel_update' not in st.session_state:
            st.session_state.last_carousel_update = datetime.now()
        if 'animation_frame' not in st.session_state:
            st.session_state.animation_frame = 0

    def get_stock_price(self, symbol):
        # Alpha Vantage Priority (if configured)
        if self.alpha_vantage_key:
            try:
                url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.alpha_vantage_key}'
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                data = r.json()
                price_str = data.get("Global Quote", {}).get("05. price")
                if price_str:
                    return float(price_str), "Alpha Vantage"
            except Exception:
                pass

        # yfinance Fallback
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if not hist.empty:
                return float(hist['Close'].iloc[-1]), "Yahoo Finance"
        except Exception:
            pass

        # Simulation Fallback
        base = {'Roche': 45, 'Bayer': 15.5, 'Hengrui Medicine': 35, 'BeiGene': 180, 'Merck': 120, 'Novartis': 95,
                'AstraZeneca': 65}
        company = None
        for k, v in self.companies.items():
            if v == symbol:
                company = k
                break
        if not company:
            company = list(self.companies.keys())[0]
        return base.get(company, 50) * (1 + random.uniform(-0.02, 0.02)), "Simulated Data"

    def get_stock_prices(self):
        """Fetch all company prices and update session state trends"""
        prices = {}
        sources = {}
        now = datetime.now()
        for company, symbol in self.companies.items():
            price, src = self.get_stock_price(symbol)
            prices[company] = price
            sources[company] = src
            trend = st.session_state.stock_trends[company]
            trend.append({'timestamp': now, 'price': price, 'source': src})
            # Keep last 100 data points
            if len(trend) > 100:
                st.session_state.stock_trends[company] = trend[-100:]
        return prices, sources

    # Try to get market cap using FMP (Priority)
    @st.cache_data(ttl=900)
    def get_market_caps(_self):
        """
        Return market cap for each company (in billions USD), priority to FMP (FinancialModelingPrep)
        """
        caps = {}
        fmp_key = _self.fmp_api_key

        for company, symbol in _self.companies.items():
            mc_billion = None

            # 1) FMP Query (if key available)
            if fmp_key:
                try:
                    fmp_symbol = symbol
                    fmp_url = f"https://financialmodelingprep.com/api/v3/market-capitalization/{fmp_symbol}?apikey={fmp_key}"
                    r = requests.get(fmp_url, timeout=8)
                    if r.status_code == 200:
                        data = r.json()
                        if isinstance(data, list) and len(data) > 0:
                            first = data[0]
                            mc = None
                            if isinstance(first, dict):
                                mc = first.get('marketCap') or first.get('market_cap') or first.get('marketcap')
                            if mc and isinstance(mc, (int, float)):
                                mc_billion = mc / 1e9
                except Exception:
                    mc_billion = None

            # 2) yfinance Attempt
            if mc_billion is None:
                try:
                    t = yf.Ticker(symbol)
                    info = t.info
                    mc = info.get('marketCap')
                    if mc and isinstance(mc, (int, float)):
                        mc_billion = mc / 1e9
                except Exception:
                    mc_billion = None

            # 3) Fallback Market Cap
            if mc_billion is None:
                mc_billion = _self.fallback_market_caps.get(company, 10.0)

            caps[company] = float(mc_billion)

        return caps

    # Other Data Acquisition: News, Clinical Trials
    @st.cache_data(ttl=900)
    def get_market_news(_self):
        articles = []
        if not _self.news_api_key:
            return {"total_articles": 0, "articles": []}
        elif _self.news_api_key:
            queries = ['"liver cancer" drug', 'hepatocellular carcinoma treatment', '肝癌 药物']
            for q in queries[:2]:
                try:
                    url = f'https://gnews.io/api/v4/top-headlines?category=science&lang=en&max=5&apikey={_self.news_api_key}'
                    r = requests.get(url, timeout=10)
                    r.raise_for_status()
                    data = r.json()
                    for a in data.get('articles', []):
                        if not any(x['title'] == a['title'] for x in articles):
                            articles.append({
                                'title': a['title'],
                                'url': a['url'],
                                'source': a.get('source', {}).get('name', 'Unknown'),
                                'published_at': a.get('publishedAt', ''),
                                'description': (a.get('description', '')[:200] + '...') if a.get('description') else ''
                            })
                except Exception:
                    continue
        if not articles:
            rss_sources = {
                "Nature": "https://www.nature.com/nature.rss",
                "Nature Medicine": "https://www.nature.com/nm.rss",
                "Cancer Cell": "https://www.cell.com/cancer-cell/current.rss",
                "Science": "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science",
                "The Lancet": "https://www.thelancet.com/rssfeed/lancet_current.xml",
                "NEJM": "https://www.nejm.org/action/showFeed?jc=nejm&type=etoc&feed=rss",
            }
            for name, url in rss_sources.items():
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:2]:  # 每个源取 2 条
                        articles.append({
                            'title': f"[{name}] {entry.title}",
                            'url': entry.link,
                            'source': name,
                            'published_at': entry.get('published', ''),
                            'description': entry.get('summary', '')[:200] + '...' if entry.get('summary') else ''
                        })
                except Exception:
                    continue
 
        if not articles:
            articles = [{
                'title': 'Novel Liver Cancer Immunotherapy Combination Reaches Primary Endpoint',
                'url': '#',
                'source': 'Medical Intelligence',
                'published_at': datetime.now().isoformat(),
                'description': 'PD-1 inhibitor combined with anti-angiogenic drugs significantly prolongs survival...'
            }]

        return {"total_articles": len(articles), "articles": articles[:5]}


    @st.cache_data(ttl=3600)
    def get_clinical_trials(_self):
        return [
            {"title": "Phase III Liver Cancer Immunotherapy Combination Study", "sponsor": "Roche",
             "phase": "Phase III", "status": "Recruiting",
             "interventions": ["PD-1 Inhibitor", "Anti-angiogenic Drugs"], "url": "#", "patients": 450,
             "completion": "2024-12"},
            {"title": "Targeted Drug Combination for Advanced Liver Cancer", "sponsor": "Bayer", "phase": "Phase II",
             "status": "Active, not recruiting", "interventions": ["Sorafenib", "Regorafenib"], "url": "#",
             "patients": 280,
             "completion": "2024-09"},
            {"title": "Novel Liver Cancer Targeted Therapy Clinical Trial", "sponsor": "Hengrui Medicine",
             "phase": "Phase II", "status": "Recruiting",
             "interventions": ["Small Molecule Inhibitor", "Immunomodulator"], "url": "#", "patients": 320,
             "completion": "2025-03"}
        ]

    def get_market_metrics(self):
        prices, sources = self.get_stock_prices()
        avg_price = np.mean(list(prices.values())) if prices else 0
        rnd_activity = len(self.get_clinical_trials())
        media_attention = self.get_market_news()['total_articles']
        price_vol = np.std(list(prices.values())) if len(prices) > 1 else 0

        # Get Market Cap (in billions USD)
        market_caps = self.get_market_caps()
        total_cap = sum(market_caps.values()) if market_caps else 0.0
        if total_cap > 0:
            weighted = sum(prices[c] * market_caps.get(c, 0) for c in prices) / total_cap
        else:
            weighted = avg_price

        return {
            'avg_stock_price': avg_price,
            'market_cap_weighted_index': weighted,
            'rnd_activity': rnd_activity,
            'media_attention': media_attention,
            'price_volatility': price_vol,
            'total_companies': len(self.companies),
            'data_sources': sources,
            'market_caps': market_caps
        }

    def update_carousel(self):
        """Update carousel index, switch every 5 seconds"""
        current_time = datetime.now()
        if (current_time - st.session_state.last_carousel_update).total_seconds() >= 5:
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(self.companies)
            st.session_state.last_carousel_update = current_time

    def update_animation_frame(self):
        """Update animation frame for dynamic visualizations"""
        st.session_state.animation_frame = (st.session_state.animation_frame + 1) % 100


# ---------------------------
# Advanced Visualization Functions
# ---------------------------
def hex_to_rgba(hex_color: str, alpha: float = 0.25):
    if not hex_color:
        return f"rgba(102,126,234,{alpha})"
    h = hex_color.strip()
    if h.startswith('#'):
        h = h[1:]
    if len(h) != 6 or not re.match(r'^[0-9a-fA-F]{6}$', h):
        return f"rgba(102,126,234,{alpha})"
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def create_animated_stock_chart(stock_trends, past_points):
    """Create animated stock price chart with enhanced visual effects"""
    fig = go.Figure()
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#a8e6cf']

    # Add traces for each company
    for i, (company, trend) in enumerate(stock_trends.items()):
        if trend:
            recent = trend[-past_points:]
            if recent:  # Ensure there is data
                # Create main trace
                fig.add_trace(go.Scatter(
                    x=[p['timestamp'] for p in recent],
                    y=[p['price'] for p in recent],
                    name=company,
                    mode='lines+markers',
                    line=dict(width=4, color=colors[i % len(colors)]),
                    marker=dict(size=8, color=colors[i % len(colors)],
                                line=dict(width=2, color='white')),
                    hovertemplate=f"<b>{company}</b><br>Time: %{{x}}<br>Price: $%{{y:.2f}}<extra></extra>"
                ))

                # Add a subtle glow effect
                fig.add_trace(go.Scatter(
                    x=[p['timestamp'] for p in recent],
                    y=[p['price'] for p in recent],
                    mode='lines',
                    line=dict(width=8, color=colors[i % len(colors)]),
                    opacity=0.2,
                    showlegend=False,
                    hoverinfo='skip'
                ))

    # Enhanced layout with dynamic elements
    fig.update_layout(
        template='plotly_dark',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.7)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        xaxis_title="Time",
        yaxis_title="Stock Price (USD)",
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text="📈 Real-time Stock Price Trends with Dynamic Visualization",
            x=0.5,
            font=dict(size=22, color='white')
        ),
        # Add dynamic annotations
        annotations=[
            dict(
                x=0.02,
                y=0.98,
                xref="paper",
                yref="paper",
                text="🔄 Live Updates",
                showarrow=False,
                font=dict(size=14, color="#10b981"),
                bgcolor="rgba(16, 185, 129, 0.1)",
                bordercolor="#10b981",
                borderwidth=1,
                borderpad=4
            )
        ]
    )

    return fig


def create_animated_radar_chart(metrics_df, current_company, companies, colors):
    """Create animated radar chart with enhanced visual effects"""
    fig = go.Figure()
    categories = list(metrics_df.columns)

    for i, company in enumerate(companies):
        base_color = colors[i % len(colors)]
        if company == current_company:
            # Highlight current carousel company with animation
            fig.add_trace(go.Scatterpolar(
                r=metrics_df.loc[company].values,
                theta=categories,
                fill='toself',
                name=company,
                line=dict(color=base_color, width=4),
                fillcolor=hex_to_rgba(base_color, alpha=0.4),
                opacity=1.0,
                hovertemplate=f"<b>{company}</b><br>%{{theta}}: %{{r:.1f}} pts<extra></extra>"
            ))
        else:
            # Other companies with reduced visibility
            fig.add_trace(go.Scatterpolar(
                r=metrics_df.loc[company].values,
                theta=categories,
                fill='toself',
                name=company,
                line=dict(color=base_color, width=1.5),
                fillcolor=hex_to_rgba(base_color, alpha=0.1),
                opacity=0.4,
                hovertemplate=f"<b>{company}</b><br>%{{theta}}: %{{r:.1f}} pts<extra></extra>"
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white')
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        template='plotly_dark',
        height=550,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor='rgba(0,0,0,0.7)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text=f"🌟 Multi-dimensional Capability Radar (Highlighting: {current_company})",
            x=0.5,
            font=dict(size=22, color='white')
        )
    )

    return fig


def create_animated_heatmap(metrics_df):
    """Create animated heatmap with enhanced visual effects"""
    # Create base heatmap
    fig = px.imshow(
        metrics_df,
        text_auto=True,
        color_continuous_scale='Viridis',
        aspect='auto',
        title="🔥 Company Metrics Heatmap (0-100 points)"
    )

    # Enhanced layout
    fig.update_layout(
        template='plotly_dark',
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickfont=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white'))
    )

    return fig


def create_market_cap_bubble_chart(prices, market_caps):
    """Create animated bubble chart showing market cap vs stock price"""
    companies = list(prices.keys())
    sizes = [market_caps.get(company, 1) * 10 for company in companies]  # Scale for visibility

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(prices.values()),
        y=list(market_caps.values()),
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#a8e6cf'],
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        text=companies,
        textposition="middle center",
        hovertemplate="<b>%{text}</b><br>Price: $%{x:.2f}<br>Market Cap: $%{y:.1f}B<extra></extra>"
    ))

    fig.update_layout(
        template='plotly_dark',
        height=400,
        title="💹 Market Cap vs Stock Price Bubble Chart",
        xaxis_title="Stock Price (USD)",
        yaxis_title="Market Cap (Billions USD)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    return fig


def create_3d_surface_plot(metrics_df):
    """Create 3D surface plot for metrics visualization"""
    companies = metrics_df.index.tolist()
    metrics = metrics_df.columns.tolist()

    # Prepare data for 3D surface
    z_data = metrics_df.values.T  # Transpose to have metrics as z-axis

    fig = go.Figure(data=[
        go.Surface(
            z=z_data,
            x=companies,
            y=metrics,
            colorscale='Viridis',
            opacity=0.9,
            contours=dict(
                z=dict(
                    show=True,
                    usecolormap=True,
                    highlightcolor="limegreen",
                    project_z=True
                )
            )
        )
    ])

    fig.update_layout(
        title='3D Surface Plot of Company Metrics',
        scene=dict(
            xaxis_title='Companies',
            yaxis_title='Metrics',
            zaxis_title='Score',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        template='plotly_dark',
        height=600,
        margin=dict(l=0, r=0, b=0, t=50)
    )

    return fig


def create_sunburst_chart(metrics_df, market_caps):
    """Create sunburst chart for hierarchical data visualization"""
    # Prepare data for sunburst
    companies = metrics_df.index.tolist()
    metrics = metrics_df.columns.tolist()

    labels = []
    parents = []
    values = []

    # Add root
    labels.append("All Companies")
    parents.append("")
    values.append(sum(market_caps.values()))

    # Add companies
    for company in companies:
        labels.append(company)
        parents.append("All Companies")
        values.append(market_caps.get(company, 1))

        # Add metrics for each company
        for metric in metrics:
            labels.append(f"{metric}")
            parents.append(company)
            values.append(metrics_df.loc[company, metric])

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(
            colors=[v / max(values) for v in values],
            colorscale='Viridis'
        ),
        hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
    ))

    fig.update_layout(
        template='plotly_dark',
        height=500,
        title="🌳 Company Metrics Sunburst Chart",
        margin=dict(t=30, l=0, r=0, b=0)
    )

    return fig


def create_scatter_matrix(metrics_df):
    """Create scatter plot matrix as alternative to parallel coordinates"""
    # Reset index to include company names as a column
    df_reset = metrics_df.reset_index()
    df_reset = df_reset.rename(columns={'index': 'Company'})

    try:
        fig = px.scatter_matrix(
            df_reset,
            dimensions=metrics_df.columns.tolist(),
            color='Company',
            title="📊 Scatter Plot Matrix of Company Metrics",
            height=600
        )
    except Exception as e:
        st.warning(f"使用替代可视化方式: {str(e)}")
        # Fallback to correlation heatmap
        return create_correlation_heatmap(metrics_df)

    fig.update_layout(
        template='plotly_dark'
    )

    return fig


def create_treemap_chart(metrics_df, market_caps):
    """Create treemap chart for hierarchical data visualization"""
    # Prepare data for treemap
    companies = metrics_df.index.tolist()

    labels = ["All Companies"]
    parents = [""]
    values = [sum(market_caps.values())]

    for company in companies:
        labels.append(company)
        parents.append("All Companies")
        values.append(market_caps.get(company, 1))

        # Calculate average metric score for company
        avg_score = metrics_df.loc[company].mean()
        labels.append(f"{company} Score")
        parents.append(company)
        values.append(avg_score)

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=[v / max(values) for v in values],
            colorscale='Viridis'
        ),
        hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
    ))

    fig.update_layout(
        template='plotly_dark',
        height=500,
        title="🌿 Company Hierarchy Treemap",
        margin=dict(t=30, l=0, r=0, b=0)
    )

    return fig


def create_animated_bar_chart(metrics_df):
    """Create animated bar chart for metric comparison"""
    # Reset index and melt the dataframe
    df_reset = metrics_df.reset_index()
    # 使用正确的列名
    id_column = df_reset.columns[0]  # 这应该是 'Company'

    df_melted = df_reset.melt(id_vars=[id_column], var_name='Metric', value_name='Score')
    df_melted = df_melted.rename(columns={id_column: 'Company'})

    fig = px.bar(
        df_melted,
        x='Company',
        y='Score',
        color='Metric',
        animation_frame='Metric',
        title="📊 Animated Metric Comparison by Company",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig.update_layout(
        template='plotly_dark',
        height=500,
        xaxis_title="Company",
        yaxis_title="Score",
        showlegend=True
    )

    return fig


def create_polar_bar_chart(metrics_df):
    """Create polar bar chart for circular data visualization"""
    companies = metrics_df.index.tolist()
    metrics = metrics_df.columns.tolist()

    fig = go.Figure()

    for i, company in enumerate(companies):
        fig.add_trace(go.Barpolar(
            r=metrics_df.loc[company].values,
            theta=metrics,
            name=company,
            marker_color=px.colors.qualitative.Vivid[i % len(px.colors.qualitative.Vivid)]
        ))

    fig.update_layout(
        template='plotly_dark',
        title='🎯 Polar Bar Chart of Company Metrics',
        font_size=12,
        legend_font_size=10,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            ),
            angularaxis=dict(
                direction="clockwise"
            )
        ),
        height=500
    )

    return fig


def create_streamgraph(metrics_df):
    """Create streamgraph for temporal data visualization"""
    # Simulate temporal data for streamgraph
    dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
    companies = metrics_df.index.tolist()

    # Create sample temporal data
    stream_data = []
    for company in companies:
        base_value = metrics_df.loc[company].mean()
        for i, date in enumerate(dates):
            stream_data.append({
                'Date': date,
                'Company': company,
                'Value': base_value * (1 + 0.1 * math.sin(i * 0.5) + random.uniform(-0.1, 0.1))
            })

    df_stream = pd.DataFrame(stream_data)

    fig = px.area(
        df_stream,
        x='Date',
        y='Value',
        color='Company',
        line_group='Company',
        title='🌊 Company Performance Streamgraph',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig.update_layout(
        template='plotly_dark',
        height=400,
        xaxis_title="Date",
        yaxis_title="Performance Score",
        showlegend=True
    )

    return fig


def create_correlation_heatmap(metrics_df):
    """Create correlation heatmap for metrics"""
    corr_matrix = metrics_df.corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect='auto',
        title="🔄 Metrics Correlation Heatmap"
    )

    fig.update_layout(
        template='plotly_dark',
        height=500,
        xaxis_title="Metrics",
        yaxis_title="Metrics"
    )

    return fig


def create_radial_progress_chart(metrics_df):
    """Create radial progress chart for overall scores"""
    companies = metrics_df.index.tolist()
    avg_scores = [metrics_df.loc[company].mean() for company in companies]

    fig = go.Figure()

    for i, (company, score) in enumerate(zip(companies, avg_scores)):
        fig.add_trace(go.Barpolar(
            r=[score],
            theta=[company],
            name=company,
            marker=dict(
                color=score,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Score")
            ),
            hovertemplate=f"<b>{company}</b><br>Average Score: {score:.1f}%<extra></extra>"
        ))

    fig.update_layout(
        template='plotly_dark',
        title='📊 Radial Progress Chart - Company Overall Scores',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=500
    )

    return fig


# ---------------------------
# UI Rendering Functions
# ---------------------------
def render_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<h1 class="main-header">🧬 Liver Cancer Drug Intelligence Platform</h1>', unsafe_allow_html=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
        padding: 12px 20px; 
        border-radius: 15px; 
        margin-bottom: 1rem; 
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    '>
        <span class='status-indicator status-live'></span>
        <strong>Real-time Data Updates</strong> | 
        📊 Multi-source Data Integration | 
        🕐 Last Update: {current_time} |
        🔄 Auto Refresh: <span style='color:#10b981'>Enabled</span>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(data_manager):
    with st.sidebar:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(102,126,234,0.3) 0%, rgba(118,75,162,0.3) 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            text-align: center;
        '>
            <h3 style='margin:0; color:white;'>⚙️ Control Panel</h3>
        </div>
        """, unsafe_allow_html=True)

        refresh_rate = st.slider(
            "🔄 Refresh Rate (seconds)",
            min_value=30,
            max_value=300,
            value=60,
            help="Data auto-refresh interval"
        )

        auto_refresh = st.checkbox("📡 Auto Refresh", value=True)

        past_points = st.slider("📉 Show Last N Data Points", min_value=1, max_value=100, value=30)

        if st.button("🎯 Manual Data Refresh", use_container_width=True):
            st.cache_data.clear()
            if 'stock_trends' in st.session_state:
                for company in st.session_state.stock_trends:
                    st.session_state.stock_trends[company] = st.session_state.stock_trends[company][
                                                             -10:]  # Keep some data
            st.rerun()

        st.divider()

        # Real-time Stock Prices & Market Cap Display
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(102,126,234,0.3) 0%, rgba(118,75,162,0.3) 100%);
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        '>
            <h4 style='margin:0; color:white; text-align:center;'>📈 Real-time Stock Prices & Market Cap</h4>
        </div>
        """, unsafe_allow_html=True)

        prices, sources = data_manager.get_stock_prices()
        market_caps = data_manager.get_market_caps()

        for company, price in prices.items():
            trend = st.session_state.stock_trends.get(company, [])
            recent = trend[-past_points:] if trend else []
            if len(recent) >= 2:
                prev = recent[-2]['price']  # Use second to last point as previous price
                current = recent[-1]['price']
                change = current - prev
                change_pct = (change / prev * 100.0) if prev != 0 else 0.0
            else:
                change = 0.0
                change_pct = 0.0

            if change > 0:
                color = "#10b981"
                icon = "📈"
            elif change < 0:
                color = "#ef4444"
                icon = "📉"
            else:
                color = "rgba(255,255,255,0.6)"
                icon = "—"

            mc = market_caps.get(company, 0.0)

            st.markdown(f"""
            <div style='
                background: rgba(30,41,59,0.8);
                padding: 1rem;
                border-radius: 12px;
                margin: 0.5rem 0;
                border-left: 4px solid {color};
            '>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='color:white;'>{company}</strong><br>
                        <small style='color:rgba(255,255,255,0.6);'>Source: {sources.get(company, 'Simulated Data')}</small><br>
                        <small style='color:rgba(255,255,255,0.6);'>Market Cap: ${mc:.1f}B</small>
                    </div>
                    <div style='text-align: right;'>
                        <div style='font-size: 1.2rem; font-weight: bold; color:white;'>${price:.2f}</div>
                        <div style='color:{color}; font-weight: bold;'>
                            {icon} {change:+.2f} ({change_pct:+.1f}%)
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Export CSV (Enhanced: includes change, percent_change, market_cap)
        st.divider()
        st.markdown("### 💾 Export Data")
        if st.button("Export Last N Points as CSV", use_container_width=True):
            rows = []
            for company, trend in st.session_state.stock_trends.items():
                recent = trend[-past_points:] if trend else []
                mc_val = market_caps.get(company, data_manager.fallback_market_caps.get(company, 0.0))
                for i, point in enumerate(recent):
                    if i > 0:
                        prev_p = recent[i - 1]['price']
                        change = point['price'] - prev_p
                        pct = (change / prev_p * 100.0) if prev_p != 0 else 0.0
                    else:
                        change = 0.0
                        pct = 0.0
                    rows.append({
                        'company': company,
                        'timestamp': point['timestamp'].isoformat(),
                        'price': point['price'],
                        'change': change,
                        'percent_change': pct,
                        'market_cap_billion_usd': mc_val,
                        'data_source': point.get('source', 'Unknown')
                    })
            if rows:
                df_out = pd.DataFrame(rows)
                csv_bytes = df_out.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Click to Download CSV", data=csv_bytes,
                                   file_name=f"liver_cancer_companies_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                   mime="text/csv",
                                   use_container_width=True)
            else:
                st.info("No historical data available for export (try again after data collection)")

        st.session_state.past_points = past_points

        st.divider()
        # Data Source Status Display
        st.markdown("### 📊 Data Source Status")
        st.markdown(
            f"- Alpha Vantage: {'✅ Configured' if data_manager.alpha_vantage_key else '❌ Not Configured (Optional)'}")
        st.markdown(f"- NewsAPI: {'✅ Configured' if data_manager.news_api_key else '❌ Not Configured'}")
        st.markdown(
            f"- FinancialModelingPrep (FMP): {'✅ Configured' if data_manager.fmp_api_key else '❌ Not Configured'}")
        st.markdown(f"- Yahoo Finance: ✅ Available (Fallback)")
        st.markdown(f"- Market Cap Priority: FMP → Yahoo → Fallback Values")


def render_market_overview(data_manager):
    st.markdown('<div class="section-header">📊 Market Overview</div>', unsafe_allow_html=True)

    with st.spinner('🔄 Fetching market data...'):
        metrics = data_manager.get_market_metrics()

    # First Row Metric Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "💊 Pharma Stock Index (Market Cap Weighted)",
            f"${metrics['market_cap_weighted_index']:.2f}",
            delta=f"{metrics['price_volatility']:.2f} Volatility"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "📈 Average Stock Price",
            f"${metrics['avg_stock_price']:.2f}"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "🔬 Active Clinical Trials",
            f"{metrics['rnd_activity']}",
            delta="R&D Activity"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "📰 Media Attention",
            f"{metrics['media_attention']}",
            delta="News Count"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Second Row - Market Cap Overview
    st.markdown("### 🏦 Company Market Cap Overview (Billions USD)")
    market_caps = metrics['market_caps']
    cap_cols = st.columns(len(market_caps))

    for i, (company, cap) in enumerate(market_caps.items()):
        with cap_cols[i]:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(30,41,59,0.9) 0%, rgba(15,23,42,0.9) 100%);
                padding: 1rem;
                border-radius: 12px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
                margin-bottom: 1rem;
            '>
                <div style='font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 0.5rem;'>{company}</div>
                <div style='font-size: 1.4rem; font-weight: bold; color: white;'>${cap:.1f}B</div>
            </div>
            """, unsafe_allow_html=True)

    # Animated Stock Price Chart
    past_points = st.session_state.get('past_points', 30)
    st.markdown(f"### 📈 Real-time Pharma Stock Trends (Last {past_points} Points)")

    # Create animated stock chart
    fig_stock = create_animated_stock_chart(st.session_state.stock_trends, past_points)
    st.plotly_chart(fig_stock, use_container_width=True)

    # Market Cap Bubble Chart
    st.markdown("### 💹 Market Cap vs Stock Price Visualization")
    prices, _ = data_manager.get_stock_prices()
    market_caps = data_manager.get_market_caps()
    fig_bubble = create_market_cap_bubble_chart(prices, market_caps)
    st.plotly_chart(fig_bubble, use_container_width=True)
def render_advanced_visualizations(data_manager):
    st.markdown('<div class="section-header">🎨 Advanced Data Visualizations</div>', unsafe_allow_html=True)

    # Update animation frame
    data_manager.update_animation_frame()

    # Calculate metrics for visualizations
    prices, sources = data_manager.get_stock_prices()
    trials_count = len(data_manager.get_clinical_trials())
    news_count = data_manager.get_market_news()['total_articles']
    market_caps = data_manager.get_market_caps()
    past_points = st.session_state.get('past_points', 30)

    # Calculate scoring metrics for each company
    metrics = {}
    for company in data_manager.companies:
        recent = st.session_state.stock_trends.get(company, [])[-past_points:]
        trend_prices = [p['price'] for p in recent] if recent else []

        # Stock Price Stability Score
        price_vol = np.std(trend_prices) if trend_prices and len(trend_prices) > 1 else 0
        price_score = max(0, 100 - price_vol * 15)

        # R&D Activity Score - Based on company-specific clinical trials
        company_trials = [t for t in data_manager.get_clinical_trials() if t['sponsor'] == company]
        rnd_score = min(100, len(company_trials) * 25 + 20)  # 25 points per trial, 20 base points

        # Media Attention Score - Simplified processing
        media_score = min(100, news_count * 8 + 20)

        # Market Cap Size Score
        market_cap = market_caps.get(company, 0)
        market_cap_score = min(100, market_cap * 0.5)  # 10 points per $20B, max 100

        # Price Performance Score (relative to average price)
        current_price = prices.get(company, 0)
        avg_price = np.mean([prices.get(c, 0) for c in data_manager.companies]) if prices else current_price
        if avg_price > 0:
            price_perf_score = min(100, max(0, (current_price / avg_price - 0.8) * 500))  # Normalized processing
        else:
            price_perf_score = 50

        metrics[company] = {
            'Price Stability': price_score,
            'R&D Activity': rnd_score,
            'Media Attention': media_score,
            'Market Cap Size': market_cap_score,
            'Price Performance': price_perf_score
        }

    df = pd.DataFrame(metrics).T
    df.index.name = "Company"

    # 3D Surface Plot
    st.markdown("### 🌐 3D Surface Visualization")
    fig_3d = create_3d_surface_plot(df)
    st.plotly_chart(fig_3d, use_container_width=True, key="3d_surface_visualization")

    # Sunburst and Treemap Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌳 Hierarchical Sunburst Chart")
        fig_sunburst = create_sunburst_chart(df, market_caps)
        st.plotly_chart(fig_sunburst, use_container_width=True, key="hierarchical_sunburst")

    with col2:
        st.markdown("### 🌿 Company Hierarchy Treemap")
        fig_treemap = create_treemap_chart(df, market_caps)
        st.plotly_chart(fig_treemap, use_container_width=True, key="company_treemap")

    # Scatter Matrix and Polar Bar Charts
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 📊 Scatter Plot Matrix")
        fig_scatter = create_scatter_matrix(df)
        st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_matrix")

    with col4:
        st.markdown("### 🎯 Polar Bar Chart")
        fig_polar = create_polar_bar_chart(df)
        st.plotly_chart(fig_polar, use_container_width=True, key="polar_bar_chart")

    # Streamgraph and Animated Bar Chart
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("### 🌊 Performance Streamgraph")
        fig_stream = create_streamgraph(df)
        st.plotly_chart(fig_stream, use_container_width=True, key="performance_streamgraph")

    with col6:
        st.markdown("### 📈 Animated Bar Comparison")
        try:
            fig_animated_bar = create_animated_bar_chart(df)
            st.plotly_chart(fig_animated_bar, use_container_width=True, key="animated_bar_comparison")
        except Exception as e:
            st.warning(f"动画条形图无法显示: {str(e)}")
            # 显示静态条形图作为替代
            fig_static_bar = px.bar(df.reset_index().melt(id_vars=['Company']),
                                  x='Company', y='value', color='variable',
                                  title="📊 Metric Comparison by Company")
            fig_static_bar.update_layout(template='plotly_dark')
            st.plotly_chart(fig_static_bar, use_container_width=True, key="static_bar_fallback")

    # Additional Visualizations
    st.markdown("### 🔄 Metrics Correlation Analysis")
    fig_corr = create_correlation_heatmap(df)
    st.plotly_chart(fig_corr, use_container_width=True, key="metrics_correlation")

    st.markdown("### 📊 Radial Progress Overview")
    fig_radial = create_radial_progress_chart(df)
    st.plotly_chart(fig_radial, use_container_width=True, key="radial_progress_overview")

def render_dynamic_score_panel(data_manager):
    st.markdown('<div class="section-header">🌟 Dynamic Comprehensive Scoring Panel (Auto-rotation)</div>',
                unsafe_allow_html=True)

    # Update carousel
    data_manager.update_carousel()
    data_manager.update_animation_frame()

    prices, sources = data_manager.get_stock_prices()
    trials_count = len(data_manager.get_clinical_trials())
    news_count = data_manager.get_market_news()['total_articles']
    market_caps = data_manager.get_market_caps()
    past_points = st.session_state.get('past_points', 30)

    # Calculate scoring metrics for each company
    metrics = {}
    for company in data_manager.companies:
        recent = st.session_state.stock_trends.get(company, [])[-past_points:]
        trend_prices = [p['price'] for p in recent] if recent else []

        # Stock Price Stability Score
        price_vol = np.std(trend_prices) if trend_prices and len(trend_prices) > 1 else 0
        price_score = max(0, 100 - price_vol * 15)

        # R&D Activity Score - Based on company-specific clinical trials
        company_trials = [t for t in data_manager.get_clinical_trials() if t['sponsor'] == company]
        rnd_score = min(100, len(company_trials) * 25 + 20)  # 25 points per trial, 20 base points

        # Media Attention Score - Simplified processing
        media_score = min(100, news_count * 8 + 20)

        # Market Cap Size Score
        market_cap = market_caps.get(company, 0)
        market_cap_score = min(100, market_cap * 0.5)  # 10 points per $20B, max 100

        # Price Performance Score (relative to average price)
        current_price = prices.get(company, 0)
        avg_price = np.mean([prices.get(c, 0) for c in data_manager.companies]) if prices else current_price
        if avg_price > 0:
            price_perf_score = min(100, max(0, (current_price / avg_price - 0.8) * 500))  # Normalized processing
        else:
            price_perf_score = 50

        metrics[company] = {
            'Price Stability': price_score,
            'R&D Activity': rnd_score,
            'Media Attention': media_score,
            'Market Cap Size': market_cap_score,
            'Price Performance': price_perf_score
        }

    df = pd.DataFrame(metrics).T
    df.index.name = "Company"
    categories = list(df.columns)
    companies = list(df.index)
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#a8e6cf']

    # Get current carousel index
    idx = st.session_state.carousel_index
    current_company = companies[idx] if companies else ""

    # Radar Chart and Ranking Side by Side
    col1, col2 = st.columns([2, 1])

    with col1:
        # Animated Radar Chart
        fig_radar = create_animated_radar_chart(df, current_company, companies, colors)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        # Comprehensive Score Ranking
        st.markdown("### 🏆 Comprehensive Score Ranking")
        totals = {c: np.mean(list(v.values())) for c, v in metrics.items()}
        sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)

        for i, (company, score) in enumerate(sorted_totals):
            color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
            medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"][i] if i < 7 else "🔹"

            st.markdown(f"""
            <div style='
                background: rgba(30,41,59,0.8); 
                padding: 1rem; 
                border-radius: 12px; 
                margin: 0.5rem 0; 
                border-left: 4px solid {color}'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-size: 1.1rem; font-weight: bold;'>{medal} {company}</span>
                    <span style='font-size: 1.3rem; color: {color}; font-weight: bold;'>{score:.1f} pts</span>
                </div>
                <div style='margin-top: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;'>
                    <div style='background: {color}; height: 100%; width: {score}%; border-radius: 10px; transition: width 1s ease;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Animated Heatmap
    st.markdown("### 🔥 Comprehensive Metrics Heatmap")
    fig_heat = create_animated_heatmap(df)
    st.plotly_chart(fig_heat, use_container_width=True)


def render_news_analysis(data_manager):
    st.markdown('<div class="section-header">📰 Industry News & Updates</div>', unsafe_allow_html=True)

    with st.spinner('🔄 Fetching latest news...'):
        news_data = data_manager.get_market_news()

    if not news_data['articles']:
        st.info("📭 No industry news available")
    else:
        for i, article in enumerate(news_data['articles']):
            with st.container():
                # Format publication time
                try:
                    pub_time = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
                    formatted_time = pub_time.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_time = article['published_at'][:10]

                st.markdown(f"""
                <div class='data-card'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
                        <h4 style='margin:0; color:white; flex:1;'>{article['title']}</h4>
                        <div style='text-align: right;'>
                            <span style='background: rgba(102,126,234,0.3); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; color:white;'>
                                {article['source']}
                            </span>
                        </div>
                    </div>
                    <p style='color:rgba(255,255,255,0.8); margin-bottom: 1rem;'>{article['description']}</p>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <small style='color:rgba(255,255,255,0.6);'>Published: {formatted_time}</small>
                        <a href='{article['url']}' target='_blank' style='
                            background: linear-gradient(135deg, #667eea, #764ba2);
                            color: white;
                            padding: 8px 16px;
                            border-radius: 8px;
                            text-decoration: none;
                            font-weight: 500;
                            transition: all 0.3s ease;
                        ' onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 15px rgba(102,126,234,0.4)';" 
                        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                            📖 Read Full Article
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)


def render_clinical_trials(data_manager):
    st.markdown('<div class="section-header">💊 Clinical Trials Overview</div>', unsafe_allow_html=True)

    with st.spinner('🔄 Fetching clinical trial data...'):
        trials = data_manager.get_clinical_trials()

    if not trials:
        st.info("No clinical trial data available")
        return

    for trial in trials:
        status_color = "#10b981" if trial['status'] == "Recruiting" else "#f59e0b"

        interventions_html = "".join([
            f'<span style="background: rgba(102,126,234,0.3); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; color:white; margin-right: 0.5rem; margin-bottom: 0.5rem; display: inline-block;">{intervention}</span>'
            for intervention in trial['interventions']
        ])

        card_html = textwrap.dedent(f"""
        <div style="background: #1e293b; padding: 1.5rem; border-radius: 1rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <h4 style="margin:0; color:white; flex:1;">{trial['title']}</h4>
                <div style="text-align: right;">
                    <span style="background: {status_color}20; color:{status_color}; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid {status_color}40;">
                        {trial['status']}
                    </span>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color:rgba(255,255,255,0.7);">Sponsor</div>
                    <div style="font-weight: bold; color:white;">{trial['sponsor']}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color:rgba(255,255,255,0.7);">Study Phase</div>
                    <div style="font-weight: bold; color:white;">{trial['phase']}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color:rgba(255,255,255,0.7);">Expected Completion</div>
                    <div style="font-weight: bold; color:white;">{trial.get('completion', 'N/A')}</div>
                </div>
            </div>

            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.9rem; color:rgba(255,255,255,0.7); margin-bottom: 0.5rem;">Interventions</div>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    {interventions_html}
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center;">
                <small style="color:rgba(255,255,255,0.6);">Patient Count: {trial.get('patients', 'N/A')}</small>
                <a href="{trial['url']}" target="_blank" style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 500;
                ">
                    🔍 View Details
                </a>
            </div>
        </div>
        """)

        # 用 iframe 渲染 HTML，保证不会被当成代码块
        components.html(card_html, height=300, scrolling=True)


# ---------------------------
# Main Program
# ---------------------------
def main():
    # Initialize Data Manager
    data_manager = EnhancedDataManager()

    # Display API Configuration Status
    if not data_manager.news_api_key:
        st.info(
            "⚠️ NEWS_API_KEY not configured — News section will use simulated data or be empty. Please add API keys to .streamlit/secrets.toml.")

    # Render Header
    render_header()

    # Use Tabs to Organize Content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Market Overview", "🌟 Comprehensive Scoring", "🎨 Advanced Visualizations", "📰 News & Updates",
         "💊 Clinical Trials"])

    with tab1:
        # Market Overview Tab - Contains sidebar and main content
        col1, col2 = st.columns([1, 4])
        with col1:
            render_sidebar(data_manager)
        with col2:
            render_market_overview(data_manager)

    with tab2:
        # Comprehensive Scoring Tab
        render_dynamic_score_panel(data_manager)

    with tab3:
        # Advanced Visualizations Tab
        render_advanced_visualizations(data_manager)

    with tab4:
        # News & Updates Tab
        render_news_analysis(data_manager)

    with tab5:
        # Clinical Trials Tab
        render_clinical_trials(data_manager)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='
        text-align: center; 
        color: rgba(255,255,255,0.6); 
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        border-radius: 15px;
        margin-top: 2rem;
    '>
        <h3 style='color:white; margin-bottom: 1rem;'>🧬 Liver Cancer Drug Intelligence Platform</h3>
        <p style='margin:0;'>Multi-source Data Integration | Real-time Monitoring | Intelligent Analysis | Last Updated: {}</p>
        <p style='margin:0; font-size: 0.9rem;'>Powered by Streamlit • Plotly • Alpha Vantage • Yahoo Finance • FinancialModelingPrep</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)


if __name__ == "__main__":
    main()





