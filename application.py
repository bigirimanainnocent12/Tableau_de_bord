
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord des Ventes Super Store",
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
        padding: 0.1rem !important;
        background-color: transparent !important;
    }
    
    .stColumn > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    
    .stHorizontalBlock {
        background-color: transparent !important;
        gap: 0.3rem !important;
        border: none !important;
        box-shadow: none !important;
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
    
    regions = ['Est', 'Ouest', 'Centre', 'Sud']
    segments = ['Consommateur', 'Entreprise', 'Bureau à domicile']
    ship_modes = ['Classe Standard', 'Deuxième Classe', 'Première Classe', 'Même Jour']
    payment_modes = ['Cartes', 'En ligne', 'Contre-remboursement']
    categories = ['Fournitures de Bureau', 'Mobilier', 'Technologie']
    sub_categories = ['Classeurs', 'Chaises', 'Téléphones']
    
    data = []
    for i in range(n_records):
        order_date = pd.Timestamp(np.random.choice(dates))
        ship_date = order_date + pd.Timedelta(days=np.random.randint(1, 15))
        
        record = {
            'ID Commande': f'FR-{order_date.year}-{100000 + i}',
            'Date Commande': order_date,
            'Date Expédition': ship_date,
            'Mode Expédition': np.random.choice(ship_modes),
            'Région': np.random.choice(regions),
            'Segment': np.random.choice(segments),
            'Catégorie': np.random.choice(categories),
            'Sous-Catégorie': np.random.choice(sub_categories),
            'Ventes': np.random.uniform(10, 500),
            'Quantité': np.random.randint(1, 10),
            'Profit': np.random.uniform(-50, 200),
            'Mode Paiement': np.random.choice(payment_modes),
            'Livraison Moyenne': np.random.randint(1, 14)
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    df['Date Commande'] = pd.to_datetime(df['Date Commande'])
    df['Date Expédition'] = pd.to_datetime(df['Date Expédition'])
    df['Année'] = df['Date Commande'].dt.year
    df['Mois'] = df['Date Commande'].dt.month
    df['Mois-Année'] = df['Date Commande'].dt.to_period('M')
    
    return df

# Charger les données
df = load_data()  # Changez par load_real_data() pour utiliser vos vraies données

# Titre principal
st.markdown('<h1 class="title">Tableau de Bord des Ventes Super Store</h1>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Layout principal - graphiques circulaires sur la même ligne
# Première section: Filtre région
st.markdown("""
<div class="region-filter">
    <div class="filter-title">Région</div>
</div>
""", unsafe_allow_html=True)

selected_region = st.selectbox(
    "Sélectionner une région",
    options=['Toutes'] + list(df['Région'].unique()),
    index=0,
    key="region_filter",
    label_visibility="hidden"
)

# Filtrer les données
if selected_region != 'Toutes':
    filtered_df = df[df['Région'] == selected_region]
else:
    filtered_df = df

# Calculer les métriques
total_sales = filtered_df['Ventes'].sum()
total_profit = filtered_df['Profit'].sum()
total_quantity = filtered_df['Quantité'].sum()
avg_delivery = filtered_df['Livraison Moyenne'].mean()

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Graphiques circulaires sur la même ligne (seulement 3 colonnes)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="small-chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #74b9ff; text-align: center; margin-bottom: 15px; font-weight: bold;">Somme des Ventes par Région</h3>', unsafe_allow_html=True)
    
    region_sales = filtered_df.groupby('Région')['Ventes'].sum().reset_index()
    region_sales['Percentage'] = (region_sales['Ventes'] / region_sales['Ventes'].sum() * 100).round(0).astype(int)
    
    fig_region = px.pie(
        region_sales, 
        values='Ventes', 
        names='Région',
        color_discrete_sequence=['#00b894', '#74b9ff', '#fd79a8', '#fdcb6e']
    )
    fig_region.update_traces(
        textposition='inside', 
        textinfo='label+percent',
        textfont=dict(color='black', size=13, family='Arial Bold'),
        marker=dict(line=dict(color='#1a1d29', width=2)),
        pull=[0.05, 0.05, 0.05, 0.05]
    )
    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(color='black', size=11, family='Arial Bold')
        ),
        height=280,
        margin=dict(t=20, b=20, l=20, r=80)
    )
    st.plotly_chart(fig_region, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #74b9ff; text-align: center; margin-bottom: 15px; font-weight: bold;">Somme des Ventes par Segment</h3>', unsafe_allow_html=True)
    
    segment_sales = filtered_df.groupby('Segment')['Ventes'].sum().reset_index()
    
    fig_segment = px.pie(
        segment_sales, 
        values='Ventes', 
        names='Segment',
        color_discrete_sequence=['#74b9ff', '#fdcb6e', '#fd79a8']
    )
    fig_segment.update_traces(
        textposition='inside', 
        textinfo='label+percent',
        textfont=dict(color='black', size=13, family='Arial Bold'),
        marker=dict(line=dict(color='#1a1d29', width=2)),
        pull=[0.05, 0.05, 0.05]
    )
    fig_segment.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(color='black', size=11, family='Arial Bold')
        ),
        height=280,
        margin=dict(t=20, b=20, l=20, r=80)
    )
    st.plotly_chart(fig_segment, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="small-chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #74b9ff; text-align: center; margin-bottom: 15px; font-weight: bold;">Somme des Ventes par Mode de Paiement</h3>', unsafe_allow_html=True)
    
    payment_sales = filtered_df.groupby('Mode Paiement')['Ventes'].sum().reset_index()
    
    fig_payment = px.pie(
        payment_sales, 
        values='Ventes', 
        names='Mode Paiement',
        color_discrete_sequence=['#00b894', '#fdcb6e', '#74b9ff']
    )
    fig_payment.update_traces(
        textposition='inside', 
        textinfo='label+percent',
        textfont=dict(color='black', size=13, family='Arial Bold'),
        marker=dict(line=dict(color='#1a1d29', width=2)),
        pull=[0.05, 0.05, 0.05]
    )
    fig_payment.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(color='black', size=11, family='Arial Bold')
        ),
        height=280,
        margin=dict(t=20, b=20, l=20, r=80)
    )
    st.plotly_chart(fig_payment, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Métriques principales sur la même ligne
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
        <div class="metric-label">Ventes</div>
        <div class="metric-value">{total_sales/1000000:.1f}M</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Quantité</div>
        <div class="metric-value">{total_quantity/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Livraison Moyenne</div>
        <div class="metric-value">{avg_delivery:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Graphiques temporels et barres
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Ventes Mensuelles par Année</div>', unsafe_allow_html=True)

monthly_sales = filtered_df.groupby(['Année', 'Mois'])['Ventes'].sum().reset_index()

fig_monthly = go.Figure()

colors = ['#74b9ff', '#fdcb6e', '#00b894']
for i, year in enumerate(sorted(monthly_sales['Année'].unique())):
    year_data = monthly_sales[monthly_sales['Année'] == year]
    fig_monthly.add_trace(go.Scatter(
        x=year_data['Mois'],
        y=year_data['Ventes'],
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
st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)

# Graphique Ship Mode
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Ventes par Mode d\'Expédition</div>', unsafe_allow_html=True)

ship_mode_sales = filtered_df.groupby('Mode Expédition')['Ventes'].sum().reset_index()
ship_mode_sales = ship_mode_sales.sort_values('Ventes', ascending=True)

fig_ship = px.bar(
    ship_mode_sales,
    x='Ventes',
    y='Mode Expédition',
    orientation='h',
    color='Mode Expédition',
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
st.plotly_chart(fig_ship, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

# Quatrième ligne: Profit et sous-catégories
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Profit Mensuel par Année</div>', unsafe_allow_html=True)

monthly_profit = filtered_df.groupby(['Année', 'Mois'])['Profit'].sum().reset_index()

fig_profit = go.Figure()

colors = ['#f39c12', '#00b894', '#e74c3c']
for i, year in enumerate(sorted(monthly_profit['Année'].unique())):
    year_data = monthly_profit[monthly_profit['Année'] == year]
    fig_profit.add_trace(go.Scatter(
        x=year_data['Mois'],
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
st.plotly_chart(fig_profit, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)

# Ligne de séparation
st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Ventes par Sous-Catégorie</div>', unsafe_allow_html=True)

subcat_sales = filtered_df.groupby('Sous-Catégorie')['Ventes'].sum().reset_index()
subcat_sales = subcat_sales.sort_values('Ventes', ascending=True)

fig_subcat = px.bar(
    subcat_sales,
    x='Ventes',
    y='Sous-Catégorie',
    orientation='h',
    color='Sous-Catégorie',
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
st.plotly_chart(fig_subcat, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)
