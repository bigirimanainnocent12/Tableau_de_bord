
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Super Store Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour reproduire exactement le design
st.markdown("""
<style>
    .main {
        background-color: #1a1d29;
        color: #ffffff;
        padding: 10px;
    }
    
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 100%;
    }
    
    .element-container {
        margin-bottom: 0rem !important;
    }
    
    .stColumn {
        padding: 0.2rem !important;
    }
    
    .stColumn > div {
        background-color: transparent !important;
    }
    
    .stHorizontalBlock {
        background-color: transparent !important;
        gap: 0.5rem !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        padding: 15px;
        border-radius: 10px;
        border: none;
        text-align: center;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
        color: #74b9ff;
        margin: 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 1.2rem;
        color: #ddd;
        margin-bottom: 10px;
        font-weight: 500;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        padding: 12px;
        border-radius: 10px;
        border: none;
        margin: 5px;
        height: 360px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .small-chart-container {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        padding: 12px;
        border-radius: 10px;
        border: none;
        margin: 5px;
        height: 310px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .title {
        color: #74b9ff;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(45deg, #74b9ff, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chart-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .region-filter {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        padding: 12px;
        border-radius: 10px;
        border: none;
        margin: 5px;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .filter-title {
        color: #74b9ff;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* Masquer les éléments Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stSelectbox > div > div {
        background-color: #2d3436;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff;
    }
    
    .section-separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, #74b9ff, transparent);
        margin: 10px 0;
        border-radius: 1px;
    }
    
    /* Supprimer les espaces par défaut de Streamlit */
    .css-1d391kg, .css-12oz5g7 {
        padding: 0 !important;
    }
    
    .css-ocqkz7 {
        gap: 0.5rem !important;
    }
    
    [data-testid="column"] {
        background-color: transparent !important;
    }
    
    [data-testid="block-container"] {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* Style pour les graphiques */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    .plotly-graph-div {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données depuis le fichier Excel
@st.cache_data
def load_real_data():
    try:
        df = pd.read_excel('DONNEESS.xlsx')
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Month-Year'] = df['Order Date'].dt.to_period('M')
        df = df.dropna(subset=['Order Date', 'Sales', 'Profit'])
        return df
    except:
        return load_data()

# Fonction pour charger les données simulées
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start='2019-01-01', end='2021-12-31', freq='D')
    n_records = 5901
    
    regions = ['East', 'West', 'Central', 'South']
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    payment_modes = ['Cards', 'Online', 'COD']
    categories = ['Office Supplies', 'Furniture', 'Technology']
    sub_categories = ['Binders', 'Chairs', 'Phones']
    
    data = []
    for i in range(n_records):
        order_date = pd.Timestamp(np.random.choice(dates))
        ship_date = order_date + pd.Timedelta(days=np.random.randint(1, 15))
        
        record = {
            'Order ID': f'US-{order_date.year}-{100000 + i}',
            'Order Date': order_date,
            'Ship Date': ship_date,
            'Ship Mode': np.random.choice(ship_modes),
            'Region': np.random.choice(regions),
            'Segment': np.random.choice(segments),
            'Category': np.random.choice(categories),
            'Sub-Category': np.random.choice(sub_categories),
            'Sales': np.random.uniform(10, 500),
            'Quantity': np.random.randint(1, 10),
            'Profit': np.random.uniform(-50, 200),
            'Payment Mode': np.random.choice(payment_modes),
            'AvgDelivery': np.random.randint(1, 14)
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Month-Year'] = df['Order Date'].dt.to_period('M')
    
    return df

# Charger les données
df = load_data()  # Changez par load_real_data() pour utiliser vos vraies données

# Titre principal
st.markdown('<h1 class="title">Super Store Sales Dashboard</h1>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Layout principal - reproduire exactement l'écran
# Première ligne: 3 graphiques circulaires + filtre région + 4 métriques
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Filtre région dans le coin supérieur droit
with col4:
    st.markdown("""
    <div class="region-filter">
        <div class="filter-title">Region</div>
    </div>
    """, unsafe_allow_html=True)
    
    selected_region = st.selectbox(
        "Sélectionner une région",
        options=['All'] + list(df['Region'].unique()),
        index=0,
        key="region_filter",
        label_visibility="hidden"
    )

# Filtrer les données
if selected_region != 'All':
    filtered_df = df[df['Region'] == selected_region]
else:
    filtered_df = df

# Calculer les métriques
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_quantity = filtered_df['Quantity'].sum()
avg_delivery = filtered_df['AvgDelivery'].mean()

# Graphiques circulaires (première ligne)
with col1:
    st.markdown('<div class="small-chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Somme de Sales par Region</div>', unsafe_allow_html=True)
    
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    region_sales['Percentage'] = (region_sales['Sales'] / region_sales['Sales'].sum() * 100).round(0).astype(int)
    
    fig_region = px.pie(
        region_sales, 
        values='Sales', 
        names='Region',
        color_discrete_sequence=['#00b894', '#74b9ff', '#fd79a8', '#fdcb6e']
    )
    fig_region.update_traces(
        textposition='outside', 
        textinfo='label+percent',
        textfont=dict(color='white', size=11),
        marker=dict(line=dict(color='#1a1d29', width=2))
    )
    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        height=280,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_region, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Somme de Sales par Segment</div>', unsafe_allow_html=True)
    
    segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    
    fig_segment = px.pie(
        segment_sales, 
        values='Sales', 
        names='Segment',
        color_discrete_sequence=['#74b9ff', '#fdcb6e', '#fd79a8']
    )
    fig_segment.update_traces(
        textposition='outside', 
        textinfo='label+percent',
        textfont=dict(color='white', size=11),
        marker=dict(line=dict(color='#1a1d29', width=2))
    )
    fig_segment.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        height=280,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_segment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="small-chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Somme de Sales par Payment Mode</div>', unsafe_allow_html=True)
    
    payment_sales = filtered_df.groupby('Payment Mode')['Sales'].sum().reset_index()
    
    fig_payment = px.pie(
        payment_sales, 
        values='Sales', 
        names='Payment Mode',
        color_discrete_sequence=['#00b894', '#fdcb6e', '#74b9ff']
    )
    fig_payment.update_traces(
        textposition='outside', 
        textinfo='label+percent',
        textfont=dict(color='white', size=11),
        marker=dict(line=dict(color='#1a1d29', width=2))
    )
    fig_payment.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        height=280,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_payment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Deuxième ligne: Métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Profit</div>
        <div class="metric-value">{total_profit/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Sales</div>
        <div class="metric-value">{total_sales/1000000:.1f}M</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Quantity</div>
        <div class="metric-value">{total_quantity/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Delivery</div>
        <div class="metric-value">{avg_delivery:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Troisième ligne: Graphiques temporels et barres
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Monthly Sales by Year</div>', unsafe_allow_html=True)
    
    monthly_sales = filtered_df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    
    fig_monthly = go.Figure()
    
    colors = ['#74b9ff', '#fdcb6e', '#00b894']
    for i, year in enumerate(sorted(monthly_sales['Year'].unique())):
        year_data = monthly_sales[monthly_sales['Year'] == year]
        fig_monthly.add_trace(go.Scatter(
            x=year_data['Month'],
            y=year_data['Sales'],
            mode='lines+markers',
            name=str(year),
            line=dict(width=3, color=colors[i % len(colors)]),
            marker=dict(size=8, color=colors[i % len(colors)])
        ))
    
    fig_monthly.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            title='',
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            showgrid=True
        ),
        yaxis=dict(
            title='',
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            showgrid=True
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        height=320,
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Sales by Ship Mode</div>', unsafe_allow_html=True)
    
    ship_mode_sales = filtered_df.groupby('Ship Mode')['Sales'].sum().reset_index()
    ship_mode_sales = ship_mode_sales.sort_values('Sales', ascending=True)
    
    fig_ship = px.bar(
        ship_mode_sales,
        x='Sales',
        y='Ship Mode',
        orientation='h',
        color='Ship Mode',
        color_discrete_sequence=['#00b894', '#74b9ff', '#fd79a8', '#fdcb6e']
    )
    fig_ship.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            title=''
        ),
        yaxis=dict(
            color='white',
            title=''
        ),
        height=320,
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig_ship, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Quatrième ligne: Profit et sous-catégories
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Monthly Profit by Year</div>', unsafe_allow_html=True)
    
    monthly_profit = filtered_df.groupby(['Year', 'Month'])['Profit'].sum().reset_index()
    
    fig_profit = go.Figure()
    
    colors = ['#f39c12', '#00b894', '#e74c3c']
    for i, year in enumerate(sorted(monthly_profit['Year'].unique())):
        year_data = monthly_profit[monthly_profit['Year'] == year]
        fig_profit.add_trace(go.Scatter(
            x=year_data['Month'],
            y=year_data['Profit'],
            mode='lines+markers',
            name=str(year),
            line=dict(width=3, color=colors[i % len(colors)]),
            marker=dict(size=8, color=colors[i % len(colors)]),
            fill='tonexty' if i > 0 else None,
            fillcolor=f'rgba({int(colors[i][1:3], 16)}, {int(colors[i][3:5], 16)}, {int(colors[i][5:7], 16)}, 0.3)'
        ))
    
    fig_profit.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            title='',
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            showgrid=True
        ),
        yaxis=dict(
            title='',
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            showgrid=True
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        height=320,
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig_profit, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Sales by SubCategory</div>', unsafe_allow_html=True)
    
    subcat_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().reset_index()
    subcat_sales = subcat_sales.sort_values('Sales', ascending=True)
    
    fig_subcat = px.bar(
        subcat_sales,
        x='Sales',
        y='Sub-Category',
        orientation='h',
        color='Sub-Category',
        color_discrete_sequence=['#fd79a8', '#f39c12', '#74b9ff']
    )
    fig_subcat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            title=''
        ),
        yaxis=dict(
            color='white',
            title=''
        ),
        height=320,
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig_subcat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
