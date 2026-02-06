"""
Walmart Supply Chain Command Center — v2.0
Interactive Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page Config
st.set_page_config(
    page_title="Walmart SCCC · Supply Chain Command Center",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg-page:#f1f5f9;--bg-card:#fff;--border:#e2e8f0;--border-light:#f1f5f9;
    --text-primary:#0f172a;--text-secondary:#475569;--text-muted:#94a3b8;
    --blue:#2563eb;--blue-light:#dbeafe;--emerald:#059669;--emerald-light:#d1fae5;
    --amber:#d97706;--amber-light:#fef3c7;--rose:#dc2626;--rose-light:#fee2e2;
    --violet:#7c3aed;--violet-light:#ede9fe;--cyan:#0891b2;--cyan-light:#cffafe;
    --shadow-sm:0 1px 2px rgba(0,0,0,0.04);--shadow-md:0 4px 12px rgba(0,0,0,0.06);
    --shadow-lg:0 8px 30px rgba(0,0,0,0.08);--radius:16px;--radius-sm:10px;
}
.stApp{background:var(--bg-page)!important}
.block-container{padding:1.5rem 2rem 2rem!important;max-width:1400px!important}
*{font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif!important}
code,pre,.mono{font-family:'JetBrains Mono',monospace!important}
#MainMenu,footer{visibility:hidden}.stDeployButton{display:none}
[data-testid="stHeader"]{background:rgba(0,0,0,0)!important;backdrop-filter:none!important}

/* Sidebar: move content up */
section[data-testid="stSidebar"]{background:var(--bg-card)!important;border-right:1px solid var(--border)!important}
section[data-testid="stSidebar"] > div:first-child{padding-top:1rem!important}
section[data-testid="stSidebar"] .block-container{padding-top:0!important}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding-top:1.2rem!important}

/* Sidebar toggle button — visible, styled, hide ligature text */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="collapsedControl"]{
    visibility:visible!important;
    background:var(--blue)!important;
    border:none!important;
    border-radius:8px!important;
    width:36px!important;height:36px!important;
    box-shadow:0 2px 8px rgba(37,99,235,0.3)!important;
    z-index:999!important;
    color:transparent!important;
    font-size:0!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    position:relative!important;
    transition:all 0.2s ease!important;
    cursor:pointer!important;
}
button[data-testid="stSidebarCollapseButton"]:hover,
button[data-testid="collapsedControl"]:hover{
    background:#1d4ed8!important;
    box-shadow:0 4px 12px rgba(37,99,235,0.4)!important;
    transform:scale(1.05)!important;
}
/* Replace text with CSS arrow icon */
button[data-testid="stSidebarCollapseButton"]::after{
    content:'✕';font-size:16px;color:white!important;position:absolute;
}
button[data-testid="collapsedControl"]::after{
    content:'☰';font-size:18px;color:white!important;position:absolute;
}
/* Hide the raw ligature text inside the button */
button[data-testid="stSidebarCollapseButton"] span,
button[data-testid="collapsedControl"] span,
button[data-testid="stSidebarCollapseButton"] svg,
button[data-testid="collapsedControl"] svg,
button[data-testid="stSidebarCollapseButton"] p,
button[data-testid="collapsedControl"] p,
button[data-testid="stSidebarCollapseButton"] *:not(style)::before,
button[data-testid="collapsedControl"] *:not(style)::before{
    font-size:0!important;color:transparent!important;visibility:hidden!important;display:none!important;
}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:var(--bg-card);padding:6px;border-radius:var(--radius);box-shadow:var(--shadow-sm);border:1px solid var(--border)}
.stTabs [data-baseweb="tab"]{border-radius:var(--radius-sm);padding:10px 20px;font-weight:600;font-size:13px;color:var(--text-secondary);background:transparent;border:none}
.stTabs [data-baseweb="tab"]:hover{background:var(--bg-page);color:var(--text-primary)}
.stTabs [aria-selected="true"]{background:var(--blue)!important;color:white!important;box-shadow:0 2px 8px rgba(37,99,235,0.3)}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none}
.kpi-row{display:flex;gap:16px;margin-bottom:24px}
.kpi-card{flex:1;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 22px;box-shadow:var(--shadow-md);transition:all 0.25s ease;position:relative;overflow:hidden}
.kpi-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-2px)}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:var(--radius) var(--radius) 0 0}
.kpi-card.blue::before{background:linear-gradient(90deg,#2563eb,#60a5fa)}
.kpi-card.emerald::before{background:linear-gradient(90deg,#059669,#34d399)}
.kpi-card.rose::before{background:linear-gradient(90deg,#dc2626,#f87171)}
.kpi-card.amber::before{background:linear-gradient(90deg,#d97706,#fbbf24)}
.kpi-card.violet::before{background:linear-gradient(90deg,#7c3aed,#a78bfa)}
.kpi-card.cyan::before{background:linear-gradient(90deg,#0891b2,#22d3ee)}
.kpi-icon{font-size:28px;margin-bottom:8px}.kpi-label{font-size:12px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}
.kpi-value{font-size:26px;font-weight:800;color:var(--text-primary);line-height:1.1;margin-bottom:6px}
.kpi-sub{font-size:11px;color:var(--text-secondary);display:flex;align-items:center;gap:4px}
.kpi-badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:700;letter-spacing:0.3px}
.badge-rose{background:var(--rose-light);color:var(--rose)}.badge-amber{background:var(--amber-light);color:var(--amber)}
.badge-blue{background:var(--blue-light);color:var(--blue)}.badge-emerald{background:var(--emerald-light);color:var(--emerald)}
.badge-violet{background:var(--violet-light);color:var(--violet)}
.section-header{display:flex;align-items:center;gap:12px;margin:28px 0 16px;padding-bottom:12px;border-bottom:2px solid var(--border)}
.section-header .icon{font-size:24px}.section-header .title{font-size:18px;font-weight:700;color:var(--text-primary)}
.section-header .desc{font-size:13px;color:var(--text-secondary);margin-left:auto}
.insight-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:18px 20px;margin-bottom:12px;border-left:4px solid;box-shadow:var(--shadow-sm)}
.insight-card.critical{border-left-color:var(--rose);background:linear-gradient(135deg,#fff5f5,#fff)}
.insight-card.warning{border-left-color:var(--amber);background:linear-gradient(135deg,#fffbeb,#fff)}
.insight-card.info{border-left-color:var(--blue);background:linear-gradient(135deg,#eff6ff,#fff)}
.insight-card.success{border-left-color:var(--emerald);background:linear-gradient(135deg,#ecfdf5,#fff)}
.insight-title{font-size:13px;font-weight:700;margin-bottom:6px}.insight-text{font-size:12.5px;color:var(--text-secondary);line-height:1.5}
.store-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px;text-align:center;box-shadow:var(--shadow-sm);transition:all 0.2s ease}
.store-card:hover{box-shadow:var(--shadow-md);transform:translateY(-1px)}
.store-name{font-size:14px;font-weight:700;color:var(--text-primary);margin-bottom:8px}
.store-metric{font-size:11px;color:var(--text-secondary);margin-bottom:4px}.store-value{font-size:16px;font-weight:800;color:var(--text-primary)}
.action-table{width:100%;border-collapse:separate;border-spacing:0;border-radius:var(--radius-sm);overflow:hidden;box-shadow:var(--shadow-md)}
.action-table thead th{background:#f8fafc;padding:12px 14px;text-align:left;font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;border-bottom:2px solid var(--border)}
.action-table tbody td{padding:10px 14px;font-size:12.5px;color:var(--text-secondary);border-bottom:1px solid var(--border-light);background:white}
.action-table tbody tr:hover td{background:#f8fafc}
.priority-critical{color:var(--rose);font-weight:700}.priority-high{color:var(--amber);font-weight:700}
.money{font-family:'JetBrains Mono',monospace!important;font-weight:600}.gap-red{color:var(--rose);font-weight:600}
.hero{background:linear-gradient(135deg,#1e40af 0%,#2563eb 40%,#3b82f6 100%);border-radius:var(--radius);padding:32px 36px;margin-bottom:24px;box-shadow:0 12px 40px rgba(0,0,0,0.1);position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-50%;right:-20%;width:60%;height:200%;background:radial-gradient(ellipse,rgba(255,255,255,0.08) 0%,transparent 70%)}
.hero-title{font-size:28px;font-weight:800;color:white;margin-bottom:6px}
.hero-sub{font-size:14px;color:rgba(255,255,255,0.8);font-weight:400}
.hero-badge{display:inline-block;background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);padding:4px 14px;border-radius:20px;font-size:11px;font-weight:600;color:white;margin-top:10px;border:1px solid rgba(255,255,255,0.2)}
.stSelectbox label,.stMultiSelect label{font-weight:600!important;color:var(--text-primary)!important;font-size:13px!important}
.stDataFrame{border-radius:var(--radius-sm)!important;overflow:hidden!important;box-shadow:var(--shadow-md)!important}
</style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    d = {}
    d['kpi'] = pd.read_csv('data/kpi_metrics.csv')
    d['category'] = pd.read_csv('data/category_stats.csv')
    d['location'] = pd.read_csv('data/location_stats.csv')
    d['regional'] = pd.read_csv('data/regional_stats.csv')
    d['weather'] = pd.read_csv('data/weather_impact.csv')
    d['weekly'] = pd.read_csv('data/weekly_trends.csv')
    d['weather_var'] = pd.read_csv('data/weather_variance.csv')
    d['weather_alerts'] = pd.read_csv('data/weather_alerts.csv')
    d['action_deck'] = pd.read_csv('data/walmart_sccc_action_deck.csv')
    d['anomalies'] = pd.read_csv('data/walmart_sccc_anomaly_watchlist.csv')
    d['enriched'] = pd.read_csv('data/walmart_sccc_enriched_data.csv')
    d['action_deck_full'] = pd.read_csv('data/action_deck.csv')
    geo = {
        'Los Angeles, CA': (34.05,-118.24,'CA','Moderate Zone'),
        'Miami, FL': (25.76,-80.19,'FL','Hurricane Risk Zone'),
        'Chicago, IL': (41.88,-87.63,'IL','Winter Storm Zone'),
        'New York, NY': (40.71,-74.01,'NY','Winter Storm Zone'),
        'Dallas, TX': (32.78,-96.80,'TX','Moderate Zone'),
    }
    for col in ['lat','lon','state','weather_zone']:
        d['location'][col] = None
    for _, row in d['location'].iterrows():
        loc = row['location']
        if loc in geo:
            idx = d['location'].index[d['location']['location']==loc]
            d['location'].loc[idx,'lat'] = geo[loc][0]
            d['location'].loc[idx,'lon'] = geo[loc][1]
            d['location'].loc[idx,'state'] = geo[loc][2]
            d['location'].loc[idx,'weather_zone'] = geo[loc][3]
    return d

data = load_data()

PLT = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans, sans-serif',color='#334155',size=12),
    margin=dict(l=20,r=20,t=40,b=20),
    hoverlabel=dict(bgcolor='white',font_size=12,font_family='Plus Jakarta Sans',bordercolor='#e2e8f0'))

C = dict(blue='#2563eb',blue2='#3b82f6',blue3='#60a5fa',emerald='#059669',emerald2='#10b981',
    amber='#d97706',amber2='#f59e0b',rose='#dc2626',rose2='#f87171',
    violet='#7c3aed',violet2='#a78bfa',cyan='#0891b2',cyan2='#22d3ee',
    indigo='#4f46e5',slate='#64748b',gray='#94a3b8')

WEATHER_COLORS = {'Sunny':'#f59e0b','Cloudy':'#94a3b8','Rainy':'#3b82f6','Stormy':'#ef4444'}
WEATHER_ICONS = {'Sunny':'☀️','Cloudy':'☁️','Rainy':'🌧️','Stormy':'⛈️'}

def fm(val, prefix='$'):
    if abs(val)>=1e9: return f'{prefix}{val/1e9:.1f}B'
    if abs(val)>=1e6: return f'{prefix}{val/1e6:.1f}M'
    if abs(val)>=1e3: return f'{prefix}{val/1e3:.1f}K'
    return f'{prefix}{val:,.0f}'

def kpi_card(icon,label,value,sub='',color='blue'):
    return f'<div class="kpi-card {color}"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'

def section(icon,title,desc=''):
    st.markdown(f'<div class="section-header"><span class="icon">{icon}</span><span class="title">{title}</span><span class="desc">{desc}</span></div>',unsafe_allow_html=True)

def insight(type_,title,text):
    st.markdown(f'<div class="insight-card {type_}"><div class="insight-title">{title}</div><div class="insight-text">{text}</div></div>',unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏬 Command Center")
    st.markdown("---")
    locations = st.multiselect("📍 Store Locations",options=data['location']['location'].tolist(),default=data['location']['location'].tolist())
    weather_filter = st.multiselect("🌤️ Weather Conditions",options=data['weather']['weather'].tolist(),default=data['weather']['weather'].tolist())
    st.markdown("---")
    st.markdown("""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px;margin-top:10px;">
        <div style="font-size:12px;font-weight:700;color:#0f172a;margin-bottom:10px;">📊 Data Coverage</div>
        <div style="font-size:11px;color:#475569;line-height:1.8;">
            <b>5,000</b> transactions · <b>5</b> stores<br>
            <b>8</b> products · <b>2</b> categories<br>
            <b>4</b> weather conditions<br>
            <b>38</b> weeks · <b>Jan–Sep 2024</b>
        </div></div>""",unsafe_allow_html=True)
    st.markdown("""<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:16px;margin-top:12px;">
        <div style="font-size:12px;font-weight:700;color:#1d4ed8;margin-bottom:6px;">🤖 ML Engine</div>
        <div style="font-size:11px;color:#3b82f6;line-height:1.6;">
            Best: Ridge (α=10.0)<br>Test R²: 0.1529<br>5 Models · 15 Features
        </div></div>""",unsafe_allow_html=True)

loc_df = data['location'][data['location']['location'].isin(locations)]
wx_df = data['weather'][data['weather']['weather'].isin(weather_filter)]

# Hero Header
st.markdown("""<div class="hero"><div class="hero-title">Walmart Supply Chain Command Center</div>
    <div class="hero-sub">Real-time supply chain intelligence across 5 locations · AI-powered anomaly detection & demand forecasting</div>
    <div class="hero-badge">🔄 SCCC v2.0 · Multi-Model ML Pipeline · 3,097 Anomalies Detected</div></div>""",unsafe_allow_html=True)

# KPI Row
kpi_data = dict(zip(data['kpi']['metric'],data['kpi']['value']))
kpi_html = '<div class="kpi-row">'
kpi_html += kpi_card('💰','Revenue at Risk',fm(kpi_data.get('total_revenue_at_risk',0)),'<span class="kpi-badge badge-rose">CRITICAL EXPOSURE</span>','rose')
kpi_html += kpi_card('📦','Total Stockouts',f"{int(kpi_data.get('total_stockouts',0)):,}",f'<span class="kpi-badge badge-amber">{kpi_data.get("stockout_rate",0):.1f}% RATE</span>','amber')
kpi_html += kpi_card('🔄','Transactions',f"{int(kpi_data.get('total_transactions',0)):,}",'<span class="kpi-badge badge-blue">5 LOCATIONS</span>','blue')
kpi_html += kpi_card('⚠️','Anomalies Detected',f"{len(data['anomalies']):,}",'<span class="kpi-badge badge-violet">MULTI-METHOD</span>','violet')
kpi_html += kpi_card('🎯','Critical Actions',f"{int(kpi_data.get('critical_actions',0)):,}",f'<span class="kpi-badge badge-emerald">{fm(data["action_deck"]["Financial Impact ($)"].sum())} IMPACT</span>','emerald')
kpi_html += '</div>'
st.markdown(kpi_html,unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["📊 Overview","🗺️ Geographic","⚡ Performance","🌦️ Weather","🔍 Anomalies","🎯 Action Deck","🤖 ML Insights","💾 Data Explorer"])

# TAB 1: OVERVIEW
with tabs[0]:
    section('📈','Weekly Demand Trends','Actual vs Forecast · 38 Weeks')
    wk = data['weekly']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wk['week'],y=wk['actual_demand'],name='Actual Demand',line=dict(color=C['blue'],width=3),mode='lines',fill='tozeroy',fillcolor='rgba(37,99,235,0.08)'))
    fig.add_trace(go.Scatter(x=wk['week'],y=wk['forecast_demand'],name='Forecast Demand',line=dict(color=C['amber'],width=2.5,dash='dash'),mode='lines'))
    fig.add_trace(go.Bar(x=wk['week'],y=wk['stockouts'],name='Stockouts',marker_color=C['rose2'],opacity=0.5,yaxis='y2'))
    fig.update_layout(**PLT,height=400,
        title=dict(text='Demand Tracking & Stockout Events',font=dict(size=15,color='#0f172a')),
        yaxis=dict(title='Demand (units)',gridcolor='#f1f5f9',zeroline=False),
        yaxis2=dict(title='Stockouts',overlaying='y',side='right',gridcolor='#f1f5f9',zeroline=False),
        xaxis=dict(title='Week',gridcolor='#f1f5f9'),
        legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1,font=dict(size=11)),hovermode='x unified')
    st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=wk['week'],y=wk['revenue_at_risk'],fill='tozeroy',fillcolor='rgba(220,38,38,0.06)',
            line=dict(color=C['rose'],width=2.5),mode='lines+markers',marker=dict(size=5),
            hovertemplate='Week %{x}<br>Revenue at Risk: $%{y:,.0f}<extra></extra>'))
        fig2.update_layout(**PLT,height=320,title=dict(text='Revenue at Risk by Week',font=dict(size=14,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9',zeroline=False,tickprefix='$',tickformat=','),xaxis=dict(title='Week',gridcolor='#f1f5f9'),showlegend=False)
        st.plotly_chart(fig2,use_container_width=True)

    with c2:
        gap = wk['actual_demand']-wk['forecast_demand']
        colors_gap = [C['emerald'] if g>=0 else C['rose'] for g in gap]
        fig3 = go.Figure(go.Bar(x=wk['week'],y=gap,marker_color=colors_gap,hovertemplate='Week %{x}<br>Gap: %{y:,} units<extra></extra>'))
        fig3.add_hline(y=0,line=dict(color='#94a3b8',width=1))
        fig3.update_layout(**PLT,height=320,title=dict(text='Demand Gap (Actual − Forecast)',font=dict(size=14,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9',zeroline=False,title='Gap (units)'),xaxis=dict(title='Week',gridcolor='#f1f5f9'))
        st.plotly_chart(fig3,use_container_width=True)

    section('📋','Category & Regional Snapshot')
    c1,c2,c3 = st.columns(3)
    with c1:
        fig = go.Figure(go.Pie(labels=data['category']['category'],values=data['category']['revenue_at_risk'],hole=0.65,
            marker=dict(colors=[C['blue'],C['violet']]),textinfo='label+percent',textfont=dict(size=12),
            hovertemplate='%{label}<br>$%{value:,.0f}<extra></extra>'))
        fig.update_layout(**PLT,height=280,title=dict(text='Revenue at Risk by Category',font=dict(size=13,color='#0f172a')),
            annotations=[dict(text=fm(data['category']['revenue_at_risk'].sum()),x=0.5,y=0.5,font_size=18,font_color='#0f172a',showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig = go.Figure(go.Pie(labels=data['regional']['region'],values=data['regional']['stockouts'],hole=0.65,
            marker=dict(colors=[C['cyan'],C['amber']]),textinfo='label+percent',textfont=dict(size=12)))
        fig.update_layout(**PLT,height=280,title=dict(text='Stockouts by Region',font=dict(size=13,color='#0f172a')),
            annotations=[dict(text=f"{data['regional']['stockouts'].sum():,}",x=0.5,y=0.5,font_size=18,font_color='#0f172a',showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)
    with c3:
        cat = data['category']
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Appliances',x=['Stockout Rate','Transactions'],y=[cat.iloc[0]['stockout_rate'],cat.iloc[0]['transactions']/50],
            marker_color=C['blue'],text=[f"{cat.iloc[0]['stockout_rate']:.1f}%",f"{int(cat.iloc[0]['transactions'])}"],textposition='outside'))
        fig.add_trace(go.Bar(name='Electronics',x=['Stockout Rate','Transactions'],y=[cat.iloc[1]['stockout_rate'],cat.iloc[1]['transactions']/50],
            marker_color=C['violet'],text=[f"{cat.iloc[1]['stockout_rate']:.1f}%",f"{int(cat.iloc[1]['transactions'])}"],textposition='outside'))
        fig.update_layout(**PLT,height=280,barmode='group',title=dict(text='Category Comparison',font=dict(size=13,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9',visible=False),showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02,font=dict(size=10)))
        st.plotly_chart(fig,use_container_width=True)

# TAB 2: GEOGRAPHIC
with tabs[1]:
    section('🗺️','Geographic Command','Store performance across the United States')
    metric_choice = st.radio("Select Metric",['Revenue at Risk','Stockout Rate','Stockout Count','Avg Demand Gap'],horizontal=True,key='geo_metric')
    metric_map = {'Revenue at Risk':('revenue_at_risk','$',True),'Stockout Rate':('stockout_rate','%',False),'Stockout Count':('stockouts','',False),'Avg Demand Gap':('avg_demand_gap','',False)}
    col,sfx,is_money = metric_map[metric_choice]
    ldf = loc_df.copy()
    vals = ldf[col].values
    max_v,min_v = vals.max(),vals.min()
    sizes = 20+40*(vals-min_v)/(max_v-min_v+1e-9)
    colors_map = []
    for v in vals:
        pct = (v-min_v)/(max_v-min_v+1e-9)
        colors_map.append(C['rose'] if pct>0.66 else C['amber'] if pct>0.33 else C['emerald'])
    if is_money:
        labels = [fm(v) for v in vals]
    elif sfx=='%':
        labels = [f"{v:.1f}%" for v in vals]
    else:
        labels = [f"{v:,.0f}" for v in vals]
    US_STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
    fig = go.Figure()
    fig.add_trace(go.Choropleth(locations=US_STATES,locationmode='USA-states',z=[0]*len(US_STATES),colorscale=[[0,'#f1f5f9'],[1,'#f1f5f9']],showscale=False,hoverinfo='skip',marker_line_color='#e2e8f0',marker_line_width=1))
    store_states = ldf['state'].dropna().unique().tolist()
    fig.add_trace(go.Choropleth(locations=store_states,locationmode='USA-states',z=[1]*len(store_states),colorscale=[[0,'#dbeafe'],[1,'#dbeafe']],showscale=False,hoverinfo='skip',marker_line_color='#93c5fd',marker_line_width=2))
    fig.add_trace(go.Scattergeo(lat=ldf['lat'],lon=ldf['lon'],mode='markers+text',
        marker=dict(size=sizes,color=colors_map,opacity=0.85,line=dict(color='white',width=2)),
        text=[f"{loc.split(',')[0]}<br><b>{lbl}</b>" for loc,lbl in zip(ldf['location'],labels)],
        textposition='top center',textfont=dict(size=11,color='#0f172a',family='Plus Jakarta Sans'),
        hovertemplate='<b>%{customdata[0]}</b><br>'+f'{metric_choice}: %{{customdata[1]}}<br>'+'Region: %{customdata[2]}<br>Weather Zone: %{customdata[3]}<extra></extra>',
        customdata=list(zip(ldf['location'],labels,ldf['region'],ldf['weather_zone']))))
    fig.update_layout(**PLT,height=520,geo=dict(scope='usa',projection_type='albers usa',showlakes=True,lakecolor='#e0f2fe',showland=True,landcolor='#f8fafc',bgcolor='rgba(0,0,0,0)'),
        title=dict(text=f'{metric_choice} by Store Location',font=dict(size=16,color='#0f172a')))
    st.plotly_chart(fig,use_container_width=True)

    cols = st.columns(len(ldf))
    for i,(_,row) in enumerate(ldf.iterrows()):
        rate = row['stockout_rate']
        risk_color = C['rose'] if rate>51.5 else C['amber'] if rate>50 else C['emerald']
        risk_label = 'HIGH' if rate>51.5 else 'MEDIUM' if rate>50 else 'LOW'
        with cols[i]:
            st.markdown(f'''<div class="store-card"><div class="store-name">{row["location"]}</div>
                <div class="store-metric">Revenue at Risk</div><div class="store-value" style="color:{C['rose']}">{fm(row["revenue_at_risk"])}</div>
                <div class="store-metric" style="margin-top:8px">Stockout Rate</div><div class="store-value">{row["stockout_rate"]:.1f}%</div>
                <div style="margin-top:8px"><span class="kpi-badge" style="background:{risk_color}20;color:{risk_color}">{risk_label} RISK</span></div></div>''',unsafe_allow_html=True)

    section('🌡️','Regional Revenue at Risk','Concentration by state')
    state_data = ldf.dropna(subset=['state'])
    fig_heat = go.Figure(go.Choropleth(locations=state_data['state'],locationmode='USA-states',z=state_data['revenue_at_risk'],
        colorscale='YlOrRd',colorbar=dict(title='Revenue at Risk',tickprefix='$',tickformat=','),marker_line_color='white',marker_line_width=2,
        hovertemplate='<b>%{location}</b><br>Revenue at Risk: $%{z:,.0f}<extra></extra>'))
    bg_states = [s for s in US_STATES if s not in state_data['state'].values]
    fig_heat.add_trace(go.Choropleth(locations=bg_states,locationmode='USA-states',z=[0]*len(bg_states),colorscale=[[0,'#f8fafc'],[1,'#f8fafc']],showscale=False,hoverinfo='skip',marker_line_color='#e2e8f0',marker_line_width=1))
    fig_heat.update_layout(**PLT,height=420,geo=dict(scope='usa',projection_type='albers usa',showlakes=True,lakecolor='#e0f2fe',bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig_heat,use_container_width=True)

# TAB 3: PERFORMANCE
with tabs[2]:
    section('📊','Performance Analytics','Location & Category Breakdown')
    c1,c2 = st.columns(2)
    with c1:
        sorted_loc = loc_df.sort_values('stockout_rate',ascending=True)
        colors_bar = [C['rose'] if r>52 else C['amber'] if r>50 else C['emerald'] for r in sorted_loc['stockout_rate']]
        fig = go.Figure(go.Bar(y=sorted_loc['location'],x=sorted_loc['stockout_rate'],orientation='h',marker_color=colors_bar,
            text=[f"{r:.1f}%" for r in sorted_loc['stockout_rate']],textposition='outside',textfont=dict(size=12,color='#0f172a'),
            hovertemplate='<b>%{y}</b><br>Stockout Rate: %{x:.1f}%<extra></extra>'))
        fig.add_vline(x=50,line=dict(color=C['rose'],width=1.5,dash='dash'),annotation=dict(text='50%',font=dict(size=10,color=C['rose']),showarrow=False))
        fig.update_layout(**PLT,height=350,title=dict(text='Stockout Rate by Location',font=dict(size=14,color='#0f172a')),
            xaxis=dict(gridcolor='#f1f5f9',range=[45,56],ticksuffix='%'),yaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        sorted_rev = loc_df.sort_values('revenue_at_risk',ascending=False)
        fig = go.Figure(go.Bar(x=sorted_rev['location'],y=sorted_rev['revenue_at_risk'],
            marker=dict(color=sorted_rev['revenue_at_risk'],colorscale=[[0,'#93c5fd'],[0.5,'#3b82f6'],[1,'#1d4ed8']]),
            text=[fm(v) for v in sorted_rev['revenue_at_risk']],textposition='outside',textfont=dict(size=12,color='#0f172a'),
            hovertemplate='<b>%{x}</b><br>Revenue at Risk: $%{y:,.0f}<extra></extra>'))
        fig.update_layout(**PLT,height=350,title=dict(text='Revenue at Risk by Location',font=dict(size=14,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9',tickprefix='$',tickformat=','),xaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)

    section('🏢','Regional Comparison','Coastal vs Inland')
    reg = data['regional']
    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Stockouts',x=reg['region'],y=reg['stockouts'],marker_color=C['blue'],text=reg['stockouts'].astype(int),textposition='outside'))
        fig.add_trace(go.Bar(name='Revenue at Risk ($M)',x=reg['region'],y=reg['revenue_at_risk']/1e6,marker_color=C['rose2'],text=[fm(v) for v in reg['revenue_at_risk']],textposition='outside'))
        fig.update_layout(**PLT,height=350,barmode='group',title=dict(text='Regional Metrics',font=dict(size=14,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9'),legend=dict(orientation='h',yanchor='bottom',y=1.02,font=dict(size=11)))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        cat = data['category']
        fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'},{'type':'domain'}]],subplot_titles=['Stockouts','Revenue at Risk'])
        fig.add_trace(go.Pie(labels=cat['category'],values=cat['stockouts'],hole=0.6,marker=dict(colors=[C['blue'],C['violet']]),textinfo='label+value'),1,1)
        fig.add_trace(go.Pie(labels=cat['category'],values=cat['revenue_at_risk'],hole=0.6,marker=dict(colors=[C['emerald'],C['amber']]),textinfo='label+percent'),1,2)
        fig.update_layout(**PLT,height=350,title=dict(text='Category Split',font=dict(size=14,color='#0f172a')))
        st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        top_loc = loc_df.loc[loc_df['revenue_at_risk'].idxmax()]
        insight('critical',f'🚨 Highest Risk: {top_loc["location"]}',f'Revenue at risk of {fm(top_loc["revenue_at_risk"])} with {top_loc["stockout_rate"]:.1f}% stockout rate. Region: {top_loc["region"]}.')
    with c2:
        best_loc = loc_df.loc[loc_df['stockout_rate'].idxmin()]
        insight('success',f'✅ Best Performing: {best_loc["location"]}',f'Lowest stockout rate at {best_loc["stockout_rate"]:.1f}% with {fm(best_loc["revenue_at_risk"])} revenue at risk.')

# TAB 4: WEATHER
with tabs[3]:
    section('🌦️','Weather Intelligence','Impact analysis across conditions')
    wx = wx_df.copy()
    worst_wx = wx.loc[wx['stockout_rate'].idxmax()]
    best_wx = wx.loc[wx['stockout_rate'].idxmin()]
    highest_var = wx.loc[wx['demand_variance'].idxmax()]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f'<div class="kpi-card rose"><div class="kpi-icon">{WEATHER_ICONS.get(worst_wx["weather"],"⛈️")}</div><div class="kpi-label">Worst Condition</div><div class="kpi-value">{worst_wx["weather"]}</div><div class="kpi-sub">{worst_wx["stockout_rate"]:.1f}% stockout rate</div></div>',unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(f'<div class="kpi-card emerald"><div class="kpi-icon">{WEATHER_ICONS.get(best_wx["weather"],"☀️")}</div><div class="kpi-label">Best Condition</div><div class="kpi-value">{best_wx["weather"]}</div><div class="kpi-sub">{best_wx["stockout_rate"]:.1f}% stockout rate</div></div>',unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f'<div class="kpi-card amber"><div class="kpi-icon">📊</div><div class="kpi-label">Highest Variance</div><div class="kpi-value">{highest_var["weather"]}</div><div class="kpi-sub">σ² = {highest_var["demand_variance"]:.1f}</div></div>',unsafe_allow_html=True)
    with kpi_cols[3]:
        st.markdown(f'<div class="kpi-card blue"><div class="kpi-icon">🌐</div><div class="kpi-label">Weather-Affected</div><div class="kpi-value">{int(wx["transactions"].sum()):,}</div><div class="kpi-sub">total transactions</div></div>',unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        wx_sorted = wx.sort_values('stockout_rate',ascending=True)
        fig = go.Figure(go.Bar(x=wx_sorted['weather'],y=wx_sorted['stockout_rate'],
            marker_color=[WEATHER_COLORS.get(w,C['gray']) for w in wx_sorted['weather']],
            text=[f"{r:.1f}%" for r in wx_sorted['stockout_rate']],textposition='outside',textfont=dict(size=13,color='#0f172a')))
        fig.add_hline(y=50,line=dict(color=C['rose'],dash='dash',width=1.5),annotation=dict(text='50% threshold',font=dict(size=10,color=C['rose'])))
        fig.update_layout(**PLT,height=380,title=dict(text='Stockout Rate by Weather',font=dict(size=14,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9',range=[46,58],ticksuffix='%'),xaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig = px.treemap(wx,path=['weather'],values='revenue_at_risk',color='stockout_rate',color_continuous_scale='YlOrRd',
            custom_data=['weather','revenue_at_risk','stockout_rate'])
        fig.update_traces(texttemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{customdata[2]:.1f}% stockout',textfont=dict(size=14))
        fig.update_layout(**PLT,height=380,title=dict(text='Revenue at Risk by Weather',font=dict(size=14,color='#0f172a')),coloraxis_colorbar=dict(title='Stockout %'))
        st.plotly_chart(fig,use_container_width=True)

    section('📉','Weekly Demand Variance by Weather')
    wv = data['weather_var']
    fig = go.Figure()
    for wx_col in ['Sunny','Cloudy','Rainy','Stormy']:
        if wx_col in wv.columns:
            fig.add_trace(go.Scatter(x=wv['week'],y=wv[wx_col],name=wx_col,line=dict(color=WEATHER_COLORS.get(wx_col,C['gray']),width=2.5),mode='lines'))
    fig.add_hline(y=0,line=dict(color='#94a3b8',width=1))
    fig.update_layout(**PLT,height=360,title=dict(text='Demand Variance from Forecast',font=dict(size=14,color='#0f172a')),
        yaxis=dict(gridcolor='#f1f5f9',title='Variance (units)'),xaxis=dict(gridcolor='#f1f5f9',title='Week'),
        legend=dict(orientation='h',yanchor='bottom',y=1.02,font=dict(size=11)),hovermode='x unified')
    st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        dims = ['Stockout Rate','Demand Variance','Revenue Risk','Transactions','Demand Gap']
        for _,row in wx.iterrows():
            vals_r = [row['stockout_rate'],row['demand_variance']/wx['demand_variance'].max()*100,
                row['revenue_at_risk']/wx['revenue_at_risk'].max()*100,row['transactions']/wx['transactions'].max()*100,
                (row['avg_demand_gap']-wx['avg_demand_gap'].min())/(wx['avg_demand_gap'].max()-wx['avg_demand_gap'].min()+1e-9)*100]
            fig.add_trace(go.Scatterpolar(r=vals_r+[vals_r[0]],theta=dims+[dims[0]],name=row['weather'],
                line=dict(color=WEATHER_COLORS.get(row['weather'],C['gray']),width=2.5),fill='toself',
                fillcolor=f"rgba({int(WEATHER_COLORS.get(row['weather'],C['gray'])[1:3],16)},{int(WEATHER_COLORS.get(row['weather'],C['gray'])[3:5],16)},{int(WEATHER_COLORS.get(row['weather'],C['gray'])[5:7],16)},0.08)"))
        fig.update_layout(**PLT,height=400,title=dict(text='Multi-Dimensional Weather Profile',font=dict(size=14,color='#0f172a')),
            polar=dict(radialaxis=dict(visible=True,range=[0,100],gridcolor='#e2e8f0'),angularaxis=dict(gridcolor='#e2e8f0')),legend=dict(font=dict(size=11)))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        alert_df = data['weather_alerts']
        if not alert_df.empty:
            for _,alert in alert_df.iterrows():
                insight('warning',f'⚠️ Weather Alert: {alert["location"]}',f'{alert["description"]}. Severity: {alert["severity"].upper()}. {int(alert["items_at_risk"])} items at risk.')
        insight('info','💡 Weather Strategy',f'Rainy & Cloudy show highest stockout rates ({worst_wx["stockout_rate"]:.1f}%). Recommend +15-20% safety stock. Sunny performs best at {best_wx["stockout_rate"]:.1f}%.')

# TAB 5: ANOMALIES
with tabs[4]:
    section('🔍','Anomaly Detection',f'{len(data["anomalies"]):,} anomalies via multi-method ensemble')
    anom = data['anomalies'].copy()
    total_anom_rev = anom['revenue_at_risk'].sum()
    stockout_anoms = anom[anom['stockout_indicator']==True]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f'<div class="kpi-card violet"><div class="kpi-icon">🔍</div><div class="kpi-label">Anomalies Found</div><div class="kpi-value">{len(anom):,}</div><div class="kpi-sub">of 5,000 transactions</div></div>',unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(f'<div class="kpi-card rose"><div class="kpi-icon">💰</div><div class="kpi-label">Revenue at Risk</div><div class="kpi-value">{fm(total_anom_rev)}</div><div class="kpi-sub">anomalous transactions</div></div>',unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f'<div class="kpi-card amber"><div class="kpi-icon">📦</div><div class="kpi-label">With Stockouts</div><div class="kpi-value">{len(stockout_anoms):,}</div><div class="kpi-sub">{len(stockout_anoms)/len(anom)*100:.1f}% of anomalies</div></div>',unsafe_allow_html=True)
    with kpi_cols[3]:
        avg_gap = anom['demand_gap'].abs().mean()
        st.markdown(f'<div class="kpi-card cyan"><div class="kpi-icon">📐</div><div class="kpi-label">Avg Demand Gap</div><div class="kpi-value">{avg_gap:.0f} units</div><div class="kpi-sub">absolute deviation</div></div>',unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for loc in anom['store_location'].unique():
            subset = anom[anom['store_location']==loc]
            fig.add_trace(go.Scatter(x=subset['actual_demand'],y=subset['forecasted_demand'],mode='markers',name=loc.split(',')[0],
                marker=dict(size=6,opacity=0.6),hovertemplate=f'<b>{loc}</b><br>Actual: %{{x}}<br>Forecast: %{{y}}<extra></extra>'))
        fig.add_trace(go.Scatter(x=[0,500],y=[0,500],mode='lines',line=dict(color='#94a3b8',width=1,dash='dash'),showlegend=False))
        fig.update_layout(**PLT,height=420,title=dict(text='Actual vs Forecast — Anomalies',font=dict(size=14,color='#0f172a')),
            xaxis=dict(title='Actual Demand',gridcolor='#f1f5f9'),yaxis=dict(title='Forecasted Demand',gridcolor='#f1f5f9'),legend=dict(font=dict(size=10)))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        loc_counts = anom.groupby('store_location').agg(count=('transaction_id','count'),rev=('revenue_at_risk','sum')).sort_values('count',ascending=True).reset_index()
        fig = go.Figure(go.Bar(y=loc_counts['store_location'],x=loc_counts['count'],orientation='h',marker_color=C['violet2'],text=loc_counts['count'],textposition='outside'))
        fig.update_layout(**PLT,height=420,title=dict(text='Anomalies by Location',font=dict(size=14,color='#0f172a')),
            xaxis=dict(gridcolor='#f1f5f9',title='Count'),yaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)

    section('🏆','Top Revenue-at-Risk Anomalies')
    top_anom = anom.nlargest(15,'revenue_at_risk')
    table_html = '<table class="action-table"><thead><tr><th>#</th><th>Location</th><th>Product</th><th>Category</th><th>Weather</th><th>Actual</th><th>Forecast</th><th>Gap</th><th>Inventory</th><th>Revenue at Risk</th></tr></thead><tbody>'
    for i,(_,r) in enumerate(top_anom.iterrows()):
        wx_icon = WEATHER_ICONS.get(r['weather_conditions'],'🌤️')
        gap_class = 'gap-red' if r['demand_gap']>0 else ''
        gap_sign = '+' if r['demand_gap']>0 else ''
        table_html += f'<tr><td>{i+1}</td><td><b>{r["store_location"]}</b></td><td>{r["product_name"]}</td><td>{r["category"]}</td><td>{wx_icon} {r["weather_conditions"]}</td><td class="mono">{int(r["actual_demand"])}</td><td class="mono">{int(r["forecasted_demand"])}</td><td class="mono {gap_class}">{gap_sign}{int(r["demand_gap"])}</td><td class="mono">{int(r["inventory_level"])}</td><td class="money">{fm(r["revenue_at_risk"])}</td></tr>'
    table_html += '</tbody></table>'
    st.markdown(table_html,unsafe_allow_html=True)

    section('📦','Anomalies by Product & Weather')
    c1,c2 = st.columns(2)
    with c1:
        prod_counts = anom.groupby('product_name')['transaction_id'].count().sort_values(ascending=True).reset_index()
        prod_counts.columns = ['product','count']
        fig = go.Figure(go.Bar(y=prod_counts['product'],x=prod_counts['count'],orientation='h',marker=dict(color=prod_counts['count'],colorscale='Blues'),text=prod_counts['count'],textposition='outside'))
        fig.update_layout(**PLT,height=350,title=dict(text='Anomalies by Product',font=dict(size=14,color='#0f172a')),xaxis=dict(gridcolor='#f1f5f9'),yaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        wx_counts = anom.groupby('weather_conditions')['transaction_id'].count().sort_values(ascending=True).reset_index()
        wx_counts.columns = ['weather','count']
        fig = go.Figure(go.Bar(y=wx_counts['weather'],x=wx_counts['count'],orientation='h',
            marker_color=[WEATHER_COLORS.get(w,C['gray']) for w in wx_counts['weather']],text=wx_counts['count'],textposition='outside'))
        fig.update_layout(**PLT,height=350,title=dict(text='Anomalies by Weather',font=dict(size=14,color='#0f172a')),xaxis=dict(gridcolor='#f1f5f9'),yaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)

# TAB 6: ACTION DECK
with tabs[5]:
    section('🎯','AI Action Deck',f'{len(data["action_deck"]):,} recommendations generated')
    ad = data['action_deck']

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f'<div class="kpi-card rose"><div class="kpi-icon">💰</div><div class="kpi-label">Total Financial Impact</div><div class="kpi-value">{fm(ad["Financial Impact ($)"].sum())}</div><div class="kpi-sub"><span class="kpi-badge badge-rose">AI-ASSESSED</span></div></div>',unsafe_allow_html=True)
    with kpi_cols[1]:
        crit = len(ad[ad['Priority']=='CRITICAL'])
        st.markdown(f'<div class="kpi-card amber"><div class="kpi-icon">⚠️</div><div class="kpi-label">Critical Actions</div><div class="kpi-value">{crit:,}</div><div class="kpi-sub">{crit/len(ad)*100:.1f}% of total</div></div>',unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f'<div class="kpi-card blue"><div class="kpi-icon">📋</div><div class="kpi-label">Total Alerts</div><div class="kpi-value">{len(ad):,}</div><div class="kpi-sub"><span class="kpi-badge badge-blue">{ad["AI Recommendation"].nunique()} TYPES</span></div></div>',unsafe_allow_html=True)
    with kpi_cols[3]:
        avg_impact = ad['Financial Impact ($)'].mean()
        st.markdown(f'<div class="kpi-card emerald"><div class="kpi-icon">📊</div><div class="kpi-label">Avg Impact / Alert</div><div class="kpi-value">{fm(avg_impact)}</div><div class="kpi-sub">per recommendation</div></div>',unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        rec_impact = ad.groupby('AI Recommendation')['Financial Impact ($)'].agg(['sum','count']).sort_values('sum',ascending=True).reset_index()
        rec_impact.columns = ['recommendation','impact','count']
        colors_rec = [C['rose'],C['amber'],C['violet'],C['blue'],C['cyan'],C['emerald']][:len(rec_impact)]
        fig = go.Figure(go.Bar(y=rec_impact['recommendation'],x=rec_impact['impact'],orientation='h',marker_color=colors_rec,
            text=[f"{fm(v)} ({c} actions)" for v,c in zip(rec_impact['impact'],rec_impact['count'])],textposition='outside',textfont=dict(size=11)))
        fig.update_layout(**PLT,height=400,title=dict(text='Financial Impact by Recommendation',font=dict(size=14,color='#0f172a')),
            xaxis=dict(gridcolor='#f1f5f9',tickprefix='$',tickformat=','),yaxis=dict(gridcolor='#f1f5f9'))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        priority_counts = ad['Priority'].value_counts().reset_index()
        priority_counts.columns = ['priority','count']
        p_colors = {'CRITICAL':C['rose'],'HIGH':C['amber'],'MEDIUM':C['blue'],'LOW':C['emerald']}
        fig = go.Figure(go.Pie(labels=priority_counts['priority'],values=priority_counts['count'],hole=0.6,
            marker=dict(colors=[p_colors.get(p,C['gray']) for p in priority_counts['priority']]),textinfo='label+percent+value',textfont=dict(size=12)))
        fig.update_layout(**PLT,height=400,title=dict(text='Priority Distribution',font=dict(size=14,color='#0f172a')),
            annotations=[dict(text=f'{len(ad):,}',x=0.5,y=0.5,font_size=22,font_color='#0f172a',showarrow=False)])
        st.plotly_chart(fig,use_container_width=True)

    section('🚨','Top Critical Actions','Sorted by financial impact')
    top_actions = ad[ad['Priority']=='CRITICAL'].nlargest(15,'Financial Impact ($)')
    table_html = '<table class="action-table"><thead><tr><th>#</th><th>Priority</th><th>Location</th><th>Product</th><th>Category</th><th>Weather</th><th>Inventory</th><th>Pred. Demand</th><th>Supply Gap</th><th>Lead Time</th><th>Recommendation</th><th>Impact</th></tr></thead><tbody>'
    for i,(_,r) in enumerate(top_actions.iterrows()):
        wx_icon = WEATHER_ICONS.get(r.get('Weather',''),'🌤️')
        gap_val = r.get('Supply Gap',0)
        table_html += f'<tr><td>{i+1}</td><td><span class="priority-critical">● CRITICAL</span></td><td><b>{r["Store Location"]}</b></td><td>{r["Product"]}</td><td>{r["Category"]}</td><td>{wx_icon} {r.get("Weather","")}</td><td class="mono">{int(r["Current Inventory"])}</td><td class="mono">{r["Predicted Demand"]:.0f}</td><td class="mono gap-red">+{gap_val:.0f}</td><td class="mono">{int(r["Lead Time (Days)"])}d</td><td><span class="kpi-badge badge-rose">🚨 {r["AI Recommendation"]}</span></td><td class="money">{fm(r["Financial Impact ($)"])}</td></tr>'
    table_html += '</tbody></table>'
    st.markdown(table_html,unsafe_allow_html=True)

    section('📍','Impact by Store Location')
    loc_impact = ad.groupby('Store Location').agg(impact=('Financial Impact ($)','sum'),count=('Priority','count')).reset_index()
    cols = st.columns(len(loc_impact))
    for i,(_,r) in enumerate(loc_impact.iterrows()):
        with cols[i]:
            st.markdown(f'<div class="store-card"><div class="store-name">{r["Store Location"]}</div><div class="store-value" style="color:{C["rose"]}">{fm(r["impact"])}</div><div class="store-metric">{int(r["count"])} actions</div></div>',unsafe_allow_html=True)

# TAB 7: ML INSIGHTS
with tabs[6]:
    section('🤖','Machine Learning Insights','Multi-model evaluation with time-series cross-validation')
    model_results = pd.DataFrame({
        'Model':['Linear Regression','Ridge (α=1.0)','Ridge (α=10.0)','Random Forest','Gradient Boosting'],
        'Train R²':[0.1750,0.1750,0.1750,0.3508,0.5383],
        'Test R²':[0.1529,0.1529,0.1529,0.1332,0.1036],
        'Test MAE':[95.2,95.2,95.2,97.2,97.1],
        'Test RMSE':[112.6,112.6,112.6,113.9,115.8]})
    features_df = pd.DataFrame({
        'Feature':['demand_rolling_mean_7','demand_rolling_mean_14','demand_rolling_std_7','demand_lag_1','demand_lag_7',
            'unit_price','inventory_level','customer_income','reorder_quantity','reorder_point','transaction_hour',
            'customer_age','supplier_lead_time','coefficient_of_variation','weather_conditions_encoded'],
        'Importance':[0.3124,0.1542,0.0657,0.0618,0.0453,0.0452,0.0425,0.0411,0.0406,0.0398,0.0333,0.0325,0.0231,0.0160,0.0110],
        'Permutation':[0.1661,0.0217,-0.0020,0.0140,0.0004,0.0000,0.0018,-0.0005,0.0000,0.0023,-0.0004,-0.0030,-0.0000,-0.0001,-0.0012]})
    cv_scores = [0.1590,0.1705,0.1688,0.1739,0.1609]

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown('<div class="kpi-card blue"><div class="kpi-icon">🏆</div><div class="kpi-label">Best Model</div><div class="kpi-value" style="font-size:20px">Ridge (α=10)</div><div class="kpi-sub"><span class="kpi-badge badge-blue">⭐ SELECTED</span></div></div>',unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown('<div class="kpi-card emerald"><div class="kpi-icon">📊</div><div class="kpi-label">Test R²</div><div class="kpi-value">0.1529</div><div class="kpi-sub">Train R²: 0.1750 (low overfit ✅)</div></div>',unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown('<div class="kpi-card amber"><div class="kpi-icon">📐</div><div class="kpi-label">Test MAE</div><div class="kpi-value">95.2 units</div><div class="kpi-sub">+11% vs baseline (106.9)</div></div>',unsafe_allow_html=True)
    with kpi_cols[3]:
        st.markdown('<div class="kpi-card violet"><div class="kpi-icon">🔄</div><div class="kpi-label">Cross-Val R²</div><div class="kpi-value">0.1666</div><div class="kpi-sub">±0.0114 (5-fold TSS)</div></div>',unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Train R²',x=model_results['Model'],y=model_results['Train R²'],marker_color=C['blue2'],text=[f"{v:.4f}" for v in model_results['Train R²']],textposition='outside'))
        fig.add_trace(go.Bar(name='Test R²',x=model_results['Model'],y=model_results['Test R²'],marker_color=C['emerald2'],text=[f"{v:.4f}" for v in model_results['Test R²']],textposition='outside'))
        fig.update_layout(**PLT,height=380,barmode='group',title=dict(text='Model Comparison — R²',font=dict(size=14,color='#0f172a')),
            yaxis=dict(gridcolor='#f1f5f9',range=[0,0.65]),legend=dict(orientation='h',yanchor='bottom',y=1.02,font=dict(size=11)))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fold_colors = [C['blue'] if s>0.165 else C['amber2'] for s in cv_scores]
        fig = go.Figure(go.Bar(x=[f'Fold {i+1}' for i in range(5)],y=cv_scores,marker_color=fold_colors,text=[f"{s:.4f}" for s in cv_scores],textposition='outside'))
        fig.add_hline(y=np.mean(cv_scores),line=dict(color=C['rose'],dash='dash',width=1.5),annotation=dict(text=f'Mean: {np.mean(cv_scores):.4f}',font=dict(size=11,color=C['rose'])))
        fig.update_layout(**PLT,height=380,title=dict(text='Cross-Validation (Ridge α=10)',font=dict(size=14,color='#0f172a')),yaxis=dict(gridcolor='#f1f5f9',range=[0,0.2],title='R² Score'))
        st.plotly_chart(fig,use_container_width=True)

    section('🔬','Feature Importance','Gini + Permutation')
    feat = features_df.sort_values('Importance',ascending=True)
    fig = go.Figure(go.Bar(y=feat['Feature'],x=feat['Importance'],orientation='h',
        marker=dict(color=feat['Importance'],colorscale='Blues'),text=[f"{v:.4f}" for v in feat['Importance']],textposition='outside',textfont=dict(size=11)))
    fig.update_layout(**PLT,height=500,title=dict(text='Feature Importance (Random Forest Gini)',font=dict(size=14,color='#0f172a')),
        xaxis=dict(gridcolor='#f1f5f9',title='Importance'),yaxis=dict(gridcolor='#f1f5f9'))
    st.plotly_chart(fig,use_container_width=True)

    section('💡','Strategic Findings')
    c1,c2 = st.columns(2)
    with c1:
        insight('success','✅ v2.0 Fix: Reduced Overfitting','v1: R²=0.42 train, -0.01 test (severe overfit). v2 Ridge: R²=0.175 train, 0.153 test — much healthier. Time-based split prevents data leakage.')
        insight('info','📊 Rolling Features Dominate','demand_rolling_mean_7 (0.312) is 2× more important than demand_rolling_mean_14 (0.154). Short-term patterns are strongest predictors.')
    with c2:
        insight('warning','⚠️ Price > Weather for Demand','Price importance (0.045) is 4.1× higher than weather (0.011). Dynamic pricing should be prioritized over weather-responsive inventory alone.')
        insight('critical','🎯 Rule-Based Engine Adds Value',f'While ML R² is 0.15, the rule-based Action Deck identified {len(ad):,} alerts worth {fm(ad["Financial Impact ($)"].sum())} — immediate operational value.')

# TAB 8: DATA EXPLORER
with tabs[7]:
    section('💾','Data Explorer','Browse all data assets')
    dataset_choice = st.selectbox("Select Dataset",['Enriched Data (5,000 transactions)','Anomaly Watchlist (3,097 items)','Action Deck — SCCC (4,003 actions)',
        'Action Deck — Full (4,015 actions)','Location Stats','Category Stats','Regional Stats','Weather Impact','Weekly Trends','Weather Variance',
        'Weather Alerts','KPI Metrics','Feature Importance','Model Results'])
    ds_map = {
        'Enriched Data (5,000 transactions)':data['enriched'],'Anomaly Watchlist (3,097 items)':data['anomalies'],
        'Action Deck — SCCC (4,003 actions)':data['action_deck'],'Action Deck — Full (4,015 actions)':data['action_deck_full'],
        'Location Stats':data['location'],'Category Stats':data['category'],'Regional Stats':data['regional'],
        'Weather Impact':data['weather'],'Weekly Trends':data['weekly'],'Weather Variance':data['weather_var'],
        'Weather Alerts':data['weather_alerts'],'KPI Metrics':data['kpi'],
        'Feature Importance':features_df,'Model Results':model_results}
    df_show = ds_map[dataset_choice]
    st.markdown(f'<span class="kpi-badge badge-blue" style="font-size:12px;padding:4px 12px;">{df_show.shape[0]} rows × {df_show.shape[1]} columns</span>',unsafe_allow_html=True)
    st.dataframe(df_show,height=450,use_container_width=True)
    csv_data = df_show.to_csv(index=False)
    st.download_button(label="📥 Download as CSV",data=csv_data,file_name=f'{dataset_choice.split("(")[0].strip().lower().replace(" ","_")}.csv',mime='text/csv')
