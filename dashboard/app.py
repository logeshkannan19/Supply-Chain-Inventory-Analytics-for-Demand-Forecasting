import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Configure the Streamlit page
st.set_page_config(page_title="Supply Chain Analytics", page_icon="📦", layout="wide")

# Load data
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
st.markdown("Analyze demand patterns, optimize inventory levels, and identify stock risks.")

if df.empty:
    st.warning("Data not found. Please run the data generation and preprocessing scripts.")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category", 
    options=np.sort(df['Category'].dropna().unique()), 
    default=df['Category'].dropna().unique()
)

region_filter = st.sidebar.multiselect(
    "Region", 
    options=np.sort(df['Region'].dropna().unique()), 
    default=df['Region'].dropna().unique()
)

min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# Map to filter
mask = (
    df['Category'].isin(category_filter) &
    df['Region'].isin(region_filter)
)
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask = mask & (df['Date'] >= start_date) & (df['Date'] <= end_date)

filtered_df = df[mask]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- Top Level KPIs ---
st.header("Executive KPIs")
col1, col2, col3, col4 = st.columns(4)

total_demand = filtered_df['Demand (Units Sold)'].sum()
current_inventory = filtered_df.sort_values('Date').groupby('Product ID').tail(1)['Inventory Level'].sum()

stock_out_count = len(filtered_df[filtered_df['Stock Status'] == 'Out of Stock'])
stock_out_rate = stock_out_count / len(filtered_df) if len(filtered_df) > 0 else 0

avg_turnover = filtered_df['Inventory Turnover Ratio'].replace([np.inf, -np.inf], np.nan).mean()

col1.metric("Total Demand", f"{total_demand:,.0f} Units")
col2.metric("Current Inventory", f"{current_inventory:,.0f} Units")
col3.metric("Stock-Out Rate", f"{stock_out_rate:.2%}")
col4.metric("Avg Inventory Turnover", f"{avg_turnover:.2f}")

# --- Core Visualizations ---
st.markdown("---")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Demand & Inventory Trends")
    # Monthly aggregation
    trend_df = filtered_df.set_index('Date').resample('M').agg({
        'Demand (Units Sold)': 'sum',
        'Inventory Level': 'mean'
    }).reset_index()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=trend_df['Date'], y=trend_df['Demand (Units Sold)'], name='Total Demand', marker_color='indigo'))
    fig1.add_trace(go.Scatter(x=trend_df['Date'], y=trend_df['Inventory Level'], name='Avg Inventory', mode='lines+markers', marker_color='orange', yaxis='y2'))
    
    fig1.update_layout(
        yaxis=dict(title='Units Sold'),
        yaxis2=dict(title='Inventory Level', overlaying='y', side='right'),
        barmode='group',
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("Top Products by Demand")
    top_prod = filtered_df.groupby('Product Name')['Demand (Units Sold)'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_prod, x='Demand (Units Sold)', y='Product Name', orientation='h', color='Demand (Units Sold)', color_continuous_scale='Blues')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

# --- Risk Area ---
st.markdown("---")
st.subheader("⚠️ Stock Risk (Low Inventory Alerts)")
latest_stock = filtered_df.sort_values('Date').groupby('Product ID').tail(1)
risk_df = latest_stock[latest_stock['Inventory Level'] < latest_stock['Reorder Point']].copy()

if not risk_df.empty:
    risk_df['Shortfall'] = risk_df['Reorder Point'] - risk_df['Inventory Level']
    display_risk = risk_df[['Product Name', 'Category', 'Warehouse', 'Inventory Level', 'Reorder Point', 'Shortfall', 'Lead Time (days)']].sort_values(by='Shortfall', ascending=False)
    st.dataframe(display_risk, use_container_width=True)
else:
    st.success("No products are currently below their reorder points.")

# --- Forecasting ---
st.markdown("---")
st.subheader("📈 Demand Forecast (Next Week)")
if not forecast_df.empty:
    prod_map = df[['Product ID', 'Product Name', 'Category']].drop_duplicates()
    forecast_details = pd.merge(forecast_df, prod_map, on='Product ID', how='left')
    
    # Sort by highest forecasted demand
    forecast_details = forecast_details.sort_values(by='Forecasted_Demand_Next_Week', ascending=False)
    
    col_fc1, col_fc2 = st.columns([2, 1])
    with col_fc1:
        st.dataframe(forecast_details[['Product Name', 'Category', 'Forecasted_Demand_Next_Week']].head(15), use_container_width=True)
        
    with col_fc2:
        top_fc = forecast_details.head(5)
        fig3 = px.pie(top_fc, values='Forecasted_Demand_Next_Week', names='Product Name', title='Top 5 Demanded Products Next Week', hole=0.4)
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Forecast data not available. Please run the forecasting model in the pipeline.")
