import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

os.makedirs("output_charts", exist_ok=True)

np.random.seed(42)
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']
categories = ['Electronics','Clothing','Groceries','Furniture','Sports']
regions = ['North','South','East','West']

rows = []
for i in range(500):
    rows.append({
        'Order_ID': f'ORD{1000+i}',
        'Month': np.random.choice(months),
        'Category': np.random.choice(categories),
        'Region': np.random.choice(regions),
        'Units_Sold': np.random.randint(1, 50),
        'Unit_Price': np.random.randint(100, 5000),
        'Customer_Age': np.random.randint(18, 65),
        'Discount_Pct': np.random.choice([0, 5, 10, 15, 20])
    })

df = pd.DataFrame(rows)
df['Revenue'] = df['Units_Sold'] * df['Unit_Price']
df['Discounted_Revenue'] = df['Revenue'] * (1 - df['Discount_Pct']/100)

print("=== RAW DATA SAMPLE ===")
print(df.head())
print(f"\nTotal Records: {len(df)}")
print(f"Null Values:\n{df.isnull().sum()}")

df.dropna(inplace=True)
df['Month'] = pd.Categorical(df['Month'], categories=months, ordered=True)

print("\n=== DATA CLEANING DONE ===")
print(f"Clean Records: {len(df)}")

df.to_csv("output_charts/cleaned_sales_data.csv", index=False)
print("Cleaned CSV saved!")

monthly = df.groupby('Month')['Discounted_Revenue'].sum().reset_index()
category = df.groupby('Category')['Discounted_Revenue'].sum().reset_index().sort_values('Discounted_Revenue', ascending=False)
region = df.groupby('Region')['Discounted_Revenue'].sum().reset_index()
cat_units = df.groupby('Category')['Units_Sold'].sum().reset_index().sort_values('Units_Sold', ascending=False)

total_revenue = df['Discounted_Revenue'].sum()
top_category = category.iloc[0]['Category']
top_region = region.loc[region['Discounted_Revenue'].idxmax(), 'Region']
avg_order = df['Discounted_Revenue'].mean()

print(f"\n=== KEY KPIs ===")
print(f"Total Revenue:     Rs {total_revenue:,.0f}")
print(f"Top Category:      {top_category}")
print(f"Top Region:        {top_region}")
print(f"Avg Order Value:   Rs {avg_order:,.0f}")

sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Customer Sales Performance Dashboard\nVanganuru John Jasmith | Data Analytics Project',
             fontsize=16, fontweight='bold', y=0.98)

axes[0,0].bar(monthly['Month'], monthly['Discounted_Revenue']/1000,
              color='#1F4E79', edgecolor='white', linewidth=0.5)
axes[0,0].set_title('Monthly Revenue Trend (Rs 000s)', fontweight='bold')
axes[0,0].set_xlabel('Month')
axes[0,0].set_ylabel('Revenue (Rs 000s)')
axes[0,0].tick_params(axis='x', rotation=45)
for i, v in enumerate(monthly['Discounted_Revenue']/1000):
    axes[0,0].text(i, v + 10, f'{v:.0f}', ha='center', fontsize=8)

colors = ['#1F4E79','#2E75B6','#4472C4','#70AD47','#ED7D31']
axes[0,1].bar(category['Category'], category['Discounted_Revenue']/1000,
              color=colors, edgecolor='white')
axes[0,1].set_title('Revenue by Product Category (Rs 000s)', fontweight='bold')
axes[0,1].set_xlabel('Category')
axes[0,1].set_ylabel('Revenue (Rs 000s)')
axes[0,1].tick_params(axis='x', rotation=15)

wedge_colors = ['#1F4E79','#2E75B6','#4472C4','#70AD47']
axes[1,0].pie(region['Discounted_Revenue'], labels=region['Region'],
              autopct='%1.1f%%', colors=wedge_colors, startangle=90)
axes[1,0].set_title('Revenue Share by Region', fontweight='bold')

axes[1,1].barh(cat_units['Category'], cat_units['Units_Sold'],
               color='#2E75B6', edgecolor='white')
axes[1,1].set_title('Units Sold by Category', fontweight='bold')
axes[1,1].set_xlabel('Total Units Sold')
for i, v in enumerate(cat_units['Units_Sold']):
    axes[1,1].text(v + 5, i, str(v), va='center', fontsize=9)

plt.tight_layout()
plt.savefig('output_charts/sales_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nDashboard chart saved as sales_dashboard.png!")

summary = {
    'KPI': ['Total Revenue (Rs)', 'Average Order Value (Rs)', 'Top Category', 'Top Region', 'Total Orders'],
    'Value': [f"{total_revenue:,.0f}", f"{avg_order:,.0f}", top_category, top_region, len(df)]
}
summary_df = pd.DataFrame(summary)
monthly_df = monthly.copy()
monthly_df.columns = ['Month', 'Revenue (Rs)']
monthly_df['Revenue (Rs)'] = monthly_df['Revenue (Rs)'].round(0)

with pd.ExcelWriter('output_charts/sales_report.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='KPI Summary', index=False)
    monthly_df.to_excel(writer, sheet_name='Monthly Revenue', index=False)
    category.to_excel(writer, sheet_name='Category Analysis', index=False)
    region.to_excel(writer, sheet_name='Region Analysis', index=False)

print("Excel report saved as sales_report.xlsx!")
print("\n=== ALL FILES SAVED IN output_charts FOLDER ===")
print("Files ready to upload to GitHub:")
print("  - cleaned_sales_data.csv")
print("  - sales_dashboard.png")
print("  - sales_report.xlsx")
print("  - sales_analysis.py")