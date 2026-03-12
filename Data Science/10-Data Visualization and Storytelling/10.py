import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv(r"C:\Users\hpvic\Downloads\DSPRAC\10-Data Visualization and Storytelling\customer_data.csv")
print(df.head())

sns.countplot(data=df, x='gender', hue='churn')
plt.title('Churn Rate by Gender')
plt.show()

gender_churn = df.groupby('gender')['churn'].mean()
print("\nChurn rate by gender:")
print(gender_churn)

fig = px.histogram(
    df,
    x='age',
    color='churn',
    nbins=20,
    histnorm='percent',
    title='Churn Rate by Age Group'
)
fig.update_layout(xaxis_title='Age', yaxis_title='% of Customers')
fig.show()

age_bins = pd.cut(df['age'], bins=5)
age_churn = df.groupby(age_bins, observed=True)['churn'].mean()
print("\nChurn rate by age group:")
print(age_churn)

service_churn = df.groupby('service_type')['churn'].mean()
plt.pie(service_churn, labels=service_churn.index, autopct='%1.1f%%')
plt.title('Churn Rate by Service Type')
plt.show()
print("\nChurn rate by service type:")
print(service_churn)

correlation_matrix = df.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()
print("\nCorrelation with churn:")
print(correlation_matrix['churn'].sort_values(ascending=False))

fig = px.scatter(df, x='tenure', y='churn', color='churn', title='Customer Tenure vs Churn')
fig.update_layout(xaxis_title='Tenure', yaxis_title='Churn (1=Yes, 0=No)')
fig.show()

tenure_churn = df.groupby(pd.cut(df['tenure'], bins=5), observed=True)['churn'].mean()
print("\nChurn rate by tenure group:")
print(tenure_churn)

print("\nKey Insights from Data Visulatization")
print(f"1. Gender: Males churn rate = {gender_churn['Male']:.2f}, Females churn rate = {gender_churn['Female']:.2f} → Slight gender influence on churn.")
print(f"2. Age: Churn varies across age groups, with certain younger/older segments more likely to churn.")
print(f"3. Service Type: Highest churn observed in '{service_churn.idxmax()}' service type → Focus retention here.")
print(f"4. Tenure: Short-tenure customers have higher churn → Target early retention strategies.")
print(f"5. Correlation: Top factors positively correlated with churn → {correlation_matrix['churn'].sort_values(ascending=False).index[1:4].tolist()}")
