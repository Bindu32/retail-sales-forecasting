import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
final_forecast_df = pd.read_csv('final_forecast_df.csv')
test = pd.read_csv('test.csv')
final_forecast_df['ds'] = pd.to_datetime(final_forecast_df['ds'])
test['Date'] = pd.to_datetime(test['Date'])

# -----------------------------
# Assuming final_forecast_df and test are already in memory

st.title("Retail Sales Forecast Dashboard")

# -----------------------------
# Sidebar: store filter
stores = final_forecast_df['Store'].unique()
selected_stores = st.sidebar.multiselect(
    "Select Store(s)", 
    options=stores, 
    default=stores[0]
)

# -----------------------------
# Sidebar: date range slider (convert to native Python date)
min_date = final_forecast_df['ds'].min().date()
max_date = final_forecast_df['ds'].max().date()
selected_dates = st.sidebar.slider(
    "Select Date Range", 
    min_value=min_date, 
    max_value=max_date,
    value=(min_date, max_date)
)

# Convert slider selection back to datetime for filtering
start_date = pd.to_datetime(selected_dates[0])
end_date = pd.to_datetime(selected_dates[1])

# -----------------------------
# Filter forecast data
filtered_forecast = final_forecast_df[
    (final_forecast_df['Store'].isin(selected_stores)) &
    (final_forecast_df['ds'] >= start_date) &
    (final_forecast_df['ds'] <= end_date)
]

# Merge actuals if available
if 'Weekly_Sales' in test.columns:
    test_copy = test.copy()
    test_copy['ds'] = pd.to_datetime(test_copy['Date'])
    actuals = test_copy.groupby(['Store', 'ds'])['Weekly_Sales'].sum().reset_index()
    filtered_df = pd.merge(filtered_forecast, actuals, on=['Store','ds'], how='left')
    filtered_df = filtered_df.rename(columns={'Weekly_Sales':'Actual_Weekly_Sales'})
else:
    filtered_df = filtered_forecast.copy()
    filtered_df['Actual_Weekly_Sales'] = np.nan

# -----------------------------
# Plot Predicted vs Actual
st.subheader("Predicted vs Actual Weekly Sales")
plt.figure(figsize=(12,6))
for store in selected_stores:
    store_data = filtered_df[filtered_df['Store'] == store]
    plt.plot(store_data['ds'], store_data['Predicted_Weekly_Sales'], linestyle='--', label=f"Predicted Store {store}")
    if not store_data['Actual_Weekly_Sales'].isna().all():
        plt.plot(store_data['ds'], store_data['Actual_Weekly_Sales'], linestyle='-', label=f"Actual Store {store}")

# -----------------------------
# Highlight holidays
highlight_holidays = st.checkbox("Highlight Holidays", value=True)
if highlight_holidays:
    holidays_df = test[test['IsHoliday'] == True].copy()
    holidays_df['ds'] = pd.to_datetime(holidays_df['Date'])
    for store in selected_stores:
        store_holidays = holidays_df[holidays_df['Store'] == store]
        plt.scatter(
            store_holidays['ds'], 
            [filtered_df['Predicted_Weekly_Sales'].max()*1.05]*len(store_holidays),
            marker='*', color='red', s=100, label=f"Holiday Store {store}"
        )

plt.xlabel("Date")
plt.ylabel("Weekly Sales")
plt.title("Predicted vs Actual Sales with Holidays")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# -----------------------------
# Show holiday table
if highlight_holidays:
    st.subheader("Holiday Weeks")
    st.dataframe(holidays_df[['Store','Date']])
