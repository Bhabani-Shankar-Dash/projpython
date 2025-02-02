import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_sales_data(file_path):
    # Read the CSV file
    df = pd.read_csv("sales data.csv")
    
    # Check for missing values
    print("Missing values in each column:")
    print(df.isnull().sum())
    
    # Convert sales and dates columns
    df['sales'] = pd.to_numeric(df['sales'].str.replace(r'[\$,]', '', regex=True), errors='coerce')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year  # Extract year
    
    # 1. Overall Statistics
    print("\n=== Overall Business Performance ===")
    print(f"Total Orders: {len(df)}")
    print(f"Total Sales: ${df['sales'].sum():,.2f}")
    print(f"Total Profit: ${df['profit'].sum():,.2f}")
    print(f"Average Profit Margin: {(df['profit'].sum() / df['sales'].sum() * 100):.2f}%")
    
    # 2. Category Analysis
    print("\n=== Category Performance ===")
    category_stats = df.groupby('category').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).rename(columns={'order_id': 'order_count'})
    print(category_stats)
    
    # 3. Regional Analysis
    print("\n=== Regional Performance ===")
    region_stats = df.groupby('region').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).sort_values('sales', ascending=False)
    print(region_stats)
    
    # 4. Shipping Analysis
    print("\n=== Shipping Mode Distribution ===")
    shipping_stats = df['ship_mode'].value_counts()
    print(shipping_stats)
    
    # 5. Yearly Trends
    print("\n=== Yearly Performance ===")
    yearly_stats = df.groupby('year').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    })
    print(yearly_stats)
    
    # 6. Segment Analysis
    print("\n=== Customer Segment Analysis ===")
    segment_stats = df.groupby('segment').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    })
    print(segment_stats)
    
    # 7. Sub-category Analysis
    print("\n=== Top 10 Sub-categories by Sales ===")
    subcategory_stats = df.groupby('sub_category').agg({
        'sales': 'sum',
        'profit': 'sum'
    }).sort_values('sales', ascending=False).head(10)
    print(subcategory_stats)
    
    # 8. Discount Analysis
    print("\n=== Discount Impact Analysis ===")
    df['has_discount'] = df['discount'] > 0
    discount_stats = df.groupby('has_discount').agg({
        'sales': 'mean',
        'profit': 'mean'
    })
    print(discount_stats)
    
    # 9. Order Priority Analysis
    print("\n=== Order Priority Distribution ===")
    priority_stats = df['order_priority'].value_counts()
    print(priority_stats)
    
    return df

# Function to create visualizations
def create_visualizations(df):
    # Set the style for all visualizations
    plt.style.use('seaborn')
    
    # 1. Monthly Sales Trend
    plt.figure(figsize=(15, 6))
    monthly_sales = df.groupby(df['order_date'].dt.to_period('M')).agg({
        'sales': 'sum'
    }).reset_index()
    monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)
    plt.plot(monthly_sales['order_date'], monthly_sales['sales'])
    plt.title('Monthly Sales Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 2. Category Performance
    plt.figure(figsize=(10, 6))
    category_sales = df.groupby('category')[['sales', 'profit']].sum()
    category_sales.plot(kind='bar')
    plt.title('Sales and Profit by Category')
    plt.tight_layout()
    plt.show()
    
    # 3. Regional Performance
    plt.figure(figsize=(12, 6))
    region_sales = df.groupby('region')['sales'].sum().sort_values(ascending=True)
    region_sales.plot(kind='barh')
    plt.title('Sales by Region')
    plt.tight_layout()
    plt.show()
    
    # 4. Shipping