import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    h1, h2, h3 {
        color: #1e3a5f;
    }
    .stAlert {
        border-radius: 8px;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_supply_chain_data.csv')
    forecast_path = os.path.join(base_dir, 'data', 'processed', 'forecast_outputs.csv')
    
    if not os.path.exists(data_path):
        return pd.DataFrame(), pd.DataFrame()
        
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    forecast_df = pd.DataFrame()
    if os.path.exists(forecast_path):
        forecast_df = pd.read_csv(forecast_path)
        
    return df, forecast_df

df, forecast_df = load_data()

st.title("📦 Supply Chain & Inventory Analytics")
st.markdown("### Demand Forecasting & Inventory Optimization Dashboard")
st.markdown("---")

if df.empty:
    st.warning("⚠️ Data not found. Please run the data generation and preprocessing scripts first.")
    st.code("python src/generate_data.py\npython src/preprocess.py\npython src/forecasting.py", language="bash")
    st.stop()

st.sidebar.header("🔍 Filters")
st.sidebar.markdown("---")

category_filter = st.sidebar.multiselect(
    "Product Category", 
    options=sorted(df['Category'].dropna().unique()),
    default=df['Category'].dropna().unique()
)

region_filter = st.sidebar.multiselect(
    "Region", 
    options=sorted(df['Region'].dropna().unique()),
    default=df['Region'].dropna().unique()
)

warehouse_filter = st.sidebar.multiselect(
    "Warehouse",
    options=sorted(df['Warehouse'].dropna().unique()),
    default=df['Warehouse'].dropna().unique()
)

min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Total Records", f"{len(df):,}")
st.sidebar.metric("Unique Products", df['Product ID'].nunique())

mask = (
    df['Category'].isin(category_filter) &
    df['Region'].isin(region_filter) &
    df['Warehouse'].isin(warehouse_filter)
)
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask = mask & (df['Date'] >= start_date) & (df['Date'] <= end_date)

filtered_df = df[mask]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.header("📈 Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

total_demand = filtered_df['Demand (Units Sold)'].sum()
current_inventory = filtered_df.sort_values('Date').groupby('Product ID').tail(1)['Inventory Level'].sum()
stock_out_count = len(filtered_df[filtered_df['Stock Status'] == 'Out of Stock'])
stock_out_rate = stock_out_count / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
avg_turnover = filtered_df['Inventory Turnover Ratio'].replace([np.inf, -np.inf], np.nan).mean()

with col1:
    st.metric("Total Demand", f"{total_demand:,.0f} Units", delta_color="normal")
with col2:
    st.metric("Current Inventory", f"{current_inventory:,.0f} Units", delta_color="normal")
with col3:
    delta = -stock_out_rate if stock_out_rate > 5 else stock_out_rate
    st.metric("Stock-Out Rate", f"{stock_out_rate:.2f}%", delta=f"{delta:.2f}%", delta_color="inverse")
with col4:
    st.metric("Avg Inventory Turnover", f"{avg_turnover:.2f}", delta_color="normal")

st.markdown("---")

st.header("📊 Analytics Dashboard")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Demand & Inventory Trends")
    trend_df = filtered_df.set_index('Date').resample('M').agg({
        'Demand (Units Sold)': 'sum',
        'Inventory Level': 'mean'
    }).reset_index()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=trend_df['Date'], 
        y=trend_df['Demand (Units Sold)'], 
        name='Total Demand',
        marker_color='#4e79a7'
    ))
    fig1.add_trace(go.Scatter(
        x=trend_df['Date'], 
        y=trend_df['Inventory Level'], 
        name='Avg Inventory',
        mode='lines+markers',
        marker_color='#f28e2b',
        yaxis='y2',
        line=dict(width=2)
    ))
    
    fig1.update_layout(
        yaxis=dict(title='Units Sold'),
        yaxis2=dict(title='Inventory Level', overlaying='y', side='right'),
        legend=dict(x=0.01, y=0.99),
        template='plotly_white',
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("🏆 Top Products by Demand")
    top_prod = filtered_df.groupby('Product Name')['Demand (Units Sold)'].sum().nlargest(10).reset_index()
    
    fig2 = px.bar(
        top_prod, 
        x='Demand (Units Sold)', 
        y='Product Name', 
        orientation='h',
        color='Demand (Units Sold)',
        color_continuous_scale='Blues'
    )
    fig2.update_layout(
        template='plotly_white',
        height=350,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("📦 Category Distribution")
    category_dist = filtered_df.groupby('Category')['Demand (Units Sold)'].sum().reset_index()
    
    fig3 = px.pie(
        category_dist, 
        values='Demand (Units Sold)', 
        names='Category',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_layout(template='plotly_white', height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col_chart4:
    st.subheader("🏭 Inventory by Warehouse")
    warehouse_inv = filtered_df.groupby('Warehouse').agg({
        'Inventory Level': 'sum',
        'Demand (Units Sold)': 'sum'
    }).reset_index()
    
    fig4 = px.bar(
        warehouse_inv,
        x='Warehouse',
        y='Inventory Level',
        color='Warehouse',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig4.update_layout(template='plotly_white', height=350, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

st.header("⚠️ Stock Risk Analysis")

latest_stock = filtered_df.sort_values('Date').groupby('Product ID').tail(1)
risk_df = latest_stock[latest_stock['Inventory Level'] < latest_stock['Reorder Point']].copy()

if not risk_df.empty:
    risk_df['Shortfall'] = risk_df['Reorder Point'] - risk_df['Inventory Level']
    risk_df['Risk Level'] = risk_df['Shortfall'].apply(
        lambda x: '🔴 Critical' if x > 100 else ('🟡 Medium' if x > 50 else '🟢 Low')
    )
    
    display_risk = risk_df[['Product Name', 'Category', 'Warehouse', 'Inventory Level', 'Reorder Point', 'Shortfall', 'Lead Time (days)', 'Risk Level']].sort_values(by='Shortfall', ascending=False)
    
    st.dataframe(
        display_risk,
        use_container_width=True,
        column_config={
            "Inventory Level": st.column_config.NumberColumn(format="%d"),
            "Reorder Point": st.column_config.NumberColumn(format="%d"),
            "Shortfall": st.column_config.NumberColumn(format="%d"),
            "Lead Time (days)": st.column_config.NumberColumn(format="%d"),
        }
    )
    
    st.markdown(f"**Total Products at Risk:** {len(risk_df)}")
else:
    st.success("✅ No products are currently below their reorder points.")

st.markdown("---")

st.header("📈 Demand Forecast")

if not forecast_df.empty:
    prod_map = df[['Product ID', 'Product Name', 'Category']].drop_duplicates()
    forecast_details = pd.merge(forecast_df, prod_map, on='Product ID', how='left')
    forecast_details = forecast_details.sort_values(by='Forecasted_Demand_Next_Week', ascending=False)
    
    col_fc1, col_fc2 = st.columns([2, 1])
    
    with col_fc1:
        st.subheader("Next Week Demand Predictions")
        st.dataframe(
            forecast_details[['Product Name', 'Category', 'Forecasted_Demand_Next_Week']].head(15),
            use_container_width=True,
            column_config={
                "Forecasted_Demand_Next_Week": st.column_config.NumberColumn(format="%.0f units")
            }
        )
        
    with col_fc2:
        st.subheader("Demand Distribution")
        top_fc = forecast_details.head(5)
        fig_fc = px.pie(
            top_fc, 
            values='Forecasted_Demand_Next_Week', 
            names='Product Name', 
            title='Top 5 Products Next Week',
            hole=0.4
        )
        fig_fc.update_layout(template='plotly_white', height=300)
        st.plotly_chart(fig_fc, use_container_width=True)
        
    st.info("💡 Forecast generated using Linear Regression with 3-period lag features.")
else:
    st.warning("Forecast data not available. Please run the forecasting model.")
    st.code("python src/forecasting.py", language="bash")

st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: gray;'>"
    f"Supply Chain Analytics Dashboard | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    f"</div>",
    unsafe_allow_html=True
)