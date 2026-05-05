import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

os.makedirs("hr_output", exist_ok=True)

np.random.seed(10)
n = 1470

departments = ['Sales','Research & Development','Human Resources']
job_roles = ['Sales Executive','Research Scientist','Laboratory Technician',
             'Manufacturing Director','Manager','Human Resources']
education_fields = ['Life Sciences','Medical','Marketing','Technical Degree','Other']

data = {
    'EmployeeID': range(1, n+1),
    'Age': np.random.randint(18, 60, n),
    'Department': np.random.choice(departments, n, p=[0.4,0.45,0.15]),
    'JobRole': np.random.choice(job_roles, n),
    'MonthlyIncome': np.random.randint(10000, 80000, n),
    'JobSatisfaction': np.random.randint(1, 5, n),
    'WorkLifeBalance': np.random.randint(1, 5, n),
    'OverTime': np.random.choice(['Yes','No'], n, p=[0.3,0.7]),
    'YearsAtCompany': np.random.randint(0, 20, n),
    'EducationField': np.random.choice(education_fields, n),
    'PerformanceRating': np.random.randint(1, 5, n),
    'NumCompaniesWorked': np.random.randint(0, 10, n),
    'DistanceFromHome': np.random.randint(1, 30, n),
}

attrition = []
for i in range(n):
    score = 0
    if data['JobSatisfaction'][i] <= 2: score += 3
    if data['OverTime'][i] == 'Yes': score += 3
    if data['MonthlyIncome'][i] < 25000: score += 2
    if data['WorkLifeBalance'][i] <= 2: score += 2
    if data['YearsAtCompany'][i] < 2: score += 1
    if data['DistanceFromHome'][i] > 20: score += 1
    attrition.append('Yes' if score >= 5 else 'No')

data['Attrition'] = attrition
df = pd.DataFrame(data)

print("=== DATASET OVERVIEW ===")
print(f"Total Employees: {len(df)}")
print(f"Attrition Count: {df['Attrition'].value_counts().to_dict()}")
print(f"Attrition Rate: {(df['Attrition']=='Yes').mean()*100:.1f}%")
print(f"\nNull Values: {df.isnull().sum().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

df.to_csv("hr_output/hr_cleaned_data.csv", index=False)
print("\nCleaned CSV saved!")

attrition_rate = (df['Attrition']=='Yes').mean()*100
avg_income = df['MonthlyIncome'].mean()
high_risk = df[(df['JobSatisfaction']<=2) & (df['OverTime']=='Yes')]
high_risk_rate = (high_risk['Attrition']=='Yes').mean()*100
top_dept = df.groupby('Department')['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).idxmax()

print(f"\n=== KEY KPIs ===")
print(f"Overall Attrition Rate:     {attrition_rate:.1f}%")
print(f"Average Monthly Income:     Rs {avg_income:,.0f}")
print(f"High Risk Employee Rate:    {high_risk_rate:.1f}%")
print(f"Highest Attrition Dept:     {top_dept}")

sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('HR Attrition Analysis — EDA Dashboard\nVanganuru John Jasmith | Data Analytics Project',
             fontsize=16, fontweight='bold', y=0.98)

attrition_counts = df['Attrition'].value_counts()
colors = ['#1F4E79','#E74C3C']
axes[0,0].pie(attrition_counts, labels=['No Attrition','Attrition'],
              autopct='%1.1f%%', colors=colors, startangle=90)
axes[0,0].set_title('Overall Attrition Rate', fontweight='bold')

dept_attr = df.groupby('Department')['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).reset_index()
dept_attr.columns = ['Department','Attrition_Rate']
axes[0,1].bar(dept_attr['Department'], dept_attr['Attrition_Rate'],
              color=['#1F4E79','#2E75B6','#70AD47'], edgecolor='white')
axes[0,1].set_title('Attrition Rate by Department (%)', fontweight='bold')
axes[0,1].set_xlabel('Department')
axes[0,1].set_ylabel('Attrition Rate (%)')
axes[0,1].tick_params(axis='x', rotation=15)
for i, v in enumerate(dept_attr['Attrition_Rate']):
    axes[0,1].text(i, v+0.3, f'{v:.1f}%', ha='center', fontsize=9)

sat_attr = df.groupby('JobSatisfaction')['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).reset_index()
sat_attr.columns = ['JobSatisfaction','Attrition_Rate']
axes[0,2].bar(sat_attr['JobSatisfaction'], sat_attr['Attrition_Rate'],
              color='#E74C3C', edgecolor='white')
axes[0,2].set_title('Attrition by Job Satisfaction Level', fontweight='bold')
axes[0,2].set_xlabel('Job Satisfaction (1=Low, 4=High)')
axes[0,2].set_ylabel('Attrition Rate (%)')

axes[1,0].boxplot([
    df[df['Attrition']=='Yes']['MonthlyIncome'],
    df[df['Attrition']=='No']['MonthlyIncome']
], labels=['Attrition=Yes','Attrition=No'])
axes[1,0].set_title('Monthly Income vs Attrition', fontweight='bold')
axes[1,0].set_ylabel('Monthly Income (Rs)')

ot_attr = df.groupby('OverTime')['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).reset_index()
ot_attr.columns = ['OverTime','Attrition_Rate']
axes[1,1].bar(ot_attr['OverTime'], ot_attr['Attrition_Rate'],
              color=['#1F4E79','#E74C3C'], edgecolor='white', width=0.4)
axes[1,1].set_title('Attrition Rate — Overtime vs No Overtime', fontweight='bold')
axes[1,1].set_xlabel('Overtime')
axes[1,1].set_ylabel('Attrition Rate (%)')
for i, v in enumerate(ot_attr['Attrition_Rate']):
    axes[1,1].text(i, v+0.3, f'{v:.1f}%', ha='center', fontsize=10)

age_bins = pd.cut(df['Age'], bins=[18,25,35,45,60],
                  labels=['18-25','26-35','36-45','46-60'])
age_attr = df.groupby(age_bins, observed=True)['Attrition'].apply(
    lambda x: (x=='Yes').mean()*100).reset_index()
age_attr.columns = ['AgeGroup','Attrition_Rate']
axes[1,2].bar(age_attr['AgeGroup'], age_attr['Attrition_Rate'],
              color='#2E75B6', edgecolor='white')
axes[1,2].set_title('Attrition Rate by Age Group', fontweight='bold')
axes[1,2].set_xlabel('Age Group')
axes[1,2].set_ylabel('Attrition Rate (%)')

plt.tight_layout()
plt.savefig('hr_output/hr_attrition_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nHR dashboard chart saved!")

summary = {
    'KPI': ['Total Employees','Attrition Rate (%)','Avg Monthly Income (Rs)',
            'High Risk Employee Rate (%)','Highest Attrition Department'],
    'Value': [n, f"{attrition_rate:.1f}%", f"{avg_income:,.0f}",
              f"{high_risk_rate:.1f}%", top_dept]
}
summary_df = pd.DataFrame(summary)

with pd.ExcelWriter('hr_output/hr_attrition_report.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='KPI Summary', index=False)
    dept_attr.to_excel(writer, sheet_name='Department Analysis', index=False)
    sat_attr.to_excel(writer, sheet_name='Satisfaction Analysis', index=False)
    df.to_excel(writer, sheet_name='Full Dataset', index=False)

print("Excel report saved!")
print("\n=== ALL FILES SAVED IN hr_output FOLDER ===")
print("Files ready to upload to GitHub:")
print("  - hr_cleaned_data.csv")
print("  - hr_attrition_dashboard.png")
print("  - hr_attrition_report.xlsx")
print("  - hr_attrition.py")