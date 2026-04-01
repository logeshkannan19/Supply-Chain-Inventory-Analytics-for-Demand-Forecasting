import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_supply_chain_data.csv')
    report_dir = os.path.join(base_dir, 'reports')
    
    os.makedirs(report_dir, exist_ok=True)
    
    print("Loading data for EDA...")
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set seaborn style
    sns.set_theme(style="whitegrid")
    
    ### 1. Demand Trends Over Time
    print("Generating Demand Trend chart...")
    plt.figure(figsize=(15, 6))
    monthly_demand = df.groupby(df['Date'].dt.to_period('M'))['Demand (Units Sold)'].sum().reset_index()
    monthly_demand['Date'] = monthly_demand['Date'].dt.to_timestamp()
    
    sns.lineplot(data=monthly_demand, x='Date', y='Demand (Units Sold)', marker='o', color='b')
    plt.title('Monthly Total Demand Trend', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Total Units Sold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, 'demand_trend.png'))
    plt.close()
    
    ### 2. Top Products by Demand
    print("Generating Top Products chart...")
    plt.figure(figsize=(12, 6))
    top_products = df.groupby('Product Name')['Demand (Units Sold)'].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')
    plt.title('Top 10 Products by Total Demand', fontsize=16)
    plt.xlabel('Total Demand')
    plt.ylabel('Product Name')
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, 'top_products.png'))
    plt.close()
    
    ### 3. Demand vs Inventory Level (Comparison Scatter)
    print("Generating Demand vs Inventory chart...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Inventory Level', y='Demand (Units Sold)', alpha=0.5, hue='Stock Status')
    plt.title('Demand vs Inventory Level', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, 'demand_vs_inventory.png'))
    plt.close()
    
    ### 4. Correlation Heatmap
    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(8, 6))
    # Select numerical columns only
    num_cols = df[['Demand (Units Sold)', 'Inventory Level', 'Reorder Point', 
                   'Lead Time (days)', 'Order Quantity', 'Inventory Turnover Ratio']]
    corr = num_cols.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap of Supply Chain Metrics', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(report_dir, 'correlation_heatmap.png'))
    plt.close()
    
    print("EDA Complete. Visualizations saved to 'reports/' directory.")

if __name__ == "__main__":
    run_eda()
