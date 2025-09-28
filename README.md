# Retail Sales Forecasting Project

## 📌 Overview
This project focuses on **forecasting weekly retail sales** for multiple stores using **time series models (Prophet, ARIMA, LSTM)** and deploying an **interactive Streamlit dashboard** to visualize predictions vs actuals.  

The goal is to:  
- Build a **data pipeline** for preprocessing and feature engineering.  
- Train forecasting models (Prophet, ARIMA, LSTM).  
- Evaluate performance using metrics such as **MAPE / RMSE**.  
- Deploy an **interactive dashboard** to compare actual vs predicted sales and highlight holiday impacts.  

---

## Live app
https://retail-sales-forecasting-zpyb68frh9tsumanjsbfar.streamlit.app/

## Set up environment
  - Install Python 3.10+
  - Create a virtual environment (venv or conda)
  - Install core libraries:
``` bash
pip install numpy pandas matplotlib seaborn scikit-learn statsmodels pmdarima prophet tensorflow keras streamlit
```

## Project flow Structure
``` bash
sales-forecasting/
│
├── notebooks/              # Jupyter notebooks for EDA & experiments
│   └── 01_eda_and_models.ipynb
│
├── data/                   # Raw and processed datasets
│   └── walmart_sales.csv
│
├── src/                    # Python scripts for final project
│   ├── eda.py              # Data cleaning + visualization
│   ├── models.py           # ARIMA, Prophet, LSTM models
│   ├── utils.py            # Helper functions (e.g. metrics, preprocessing)
│
├── app.py                  # Streamlit app for deployment
│
├── requirements.txt        # All libraries needed
│
└── README.md               # Project overview (later)
```


##  Project Workflow
1. **Data Preparation**  
   - Loaded Walmart Weekly Sales dataset (or similar retail dataset).  
   - Cleaned missing values, encoded holiday information, and aggregated sales per store/date.  
   - Created training (`train.csv`) and test (`test.csv`) datasets.  

2. **Modeling & Forecasting**  
   - Tried multiple models:
     - **ARIMA** (classical statistical approach).  
     - **Prophet** (handles seasonality, holidays, trends).  
     - **LSTM** (deep learning).  
   - Prophet was chosen for deployment due to interpretability and holiday handling.  

3. **Evaluation**  
   - Compared predictions with actuals using error metrics.  
   - Example metric:  
     ```
     MAPE (Prophet) = 12%  
     MAPE (ARIMA)   = 15%  
     MAPE (LSTM)    = 10%  
     ```
   - Final model saved as **Prophet forecast** (`final_forecast_df.csv`).  

4. **Dashboard Development**  
   - Built with **Streamlit** (`dashboard.py`).  
   - Features:
     - Store filter (choose one or multiple stores).  
     - Date range selection.  
     - Predicted vs actual sales plot.  
     - Highlight holiday weeks with red stars.  
     - Holiday week table (store + date).  

5. **Deployment**  
   - Run locally with:  
     ```bash
     streamlit run dashboard.py
     ```  
   - Can be deployed on **Streamlit Cloud / Heroku / AWS / GCP**.  

---

## 📊 Dashboard Preview
**Features in action:**  
- Sidebar filters for store and date range.  
- Line chart comparing predicted vs actual sales.  
- Holiday markers (`*`) shown on graph.  
- Holiday weeks displayed in table format.  

---

## ⚙️ Requirements
Install dependencies:

```bash
pip install pandas numpy matplotlib streamlit prophet
```

---

## ▶️ How to Run Locally
1. Clone the repo or download project files.  
2. Place your datasets in the project folder:
   - `train.csv` → training dataset.  
   - `test.csv` → test/actuals dataset.  
   - `final_forecast_df.csv` → saved Prophet forecasts.  
3. Start the dashboard:  

```bash
streamlit run dashboard.py
```

4. Open browser at `http://localhost:8501`.

---

## 📂 File Structure
```
retail-sales-forecasting/
│
├── train.csv               # Training dataset
├── test.csv                # Test dataset with actuals
├── final_forecast_df.csv   # Forecast results from Prophet
├── dashboard.py            # Streamlit dashboard code
├── modeling.ipynb          # Jupyter Notebook with EDA, model training
└── README.md               # Project documentation
```

---

## 📑 Example Code Snippets

**Dashboard (`dashboard.py`)** – key parts:
```python
# Sidebar: Store filter
stores = final_forecast_df['Store'].unique()
selected_stores = st.sidebar.multiselect("Select Store(s)", options=stores, default=stores[0])

# Date range filter
min_date = final_forecast_df['ds'].min().date()
max_date = final_forecast_df['ds'].max().date()
selected_dates = st.sidebar.slider("Select Date Range", min_date, max_date, (min_date, max_date))

# Plot Predicted vs Actual
plt.figure(figsize=(12,6))
for store in selected_stores:
    store_data = filtered_df[filtered_df['Store'] == store]
    plt.plot(store_data['ds'], store_data['Predicted_Weekly_Sales'], linestyle='--', label=f"Predicted Store {store}")
    plt.plot(store_data['ds'], store_data['Actual_Weekly_Sales'], linestyle='-', label=f"Actual Store {store}")
```

---

## 🚀 Future Improvements
- Deploy as a **public dashboard on Streamlit Cloud**.  
- Add more advanced models (XGBoost, CatBoost).  
- Build interactive **KPIs (MAPE, RMSE)** inside the dashboard.  
- Add **store clustering** (group stores with similar sales patterns).  

---

## 📌 Conclusion
This project demonstrates **end-to-end sales forecasting**:  
- Data prep → Modeling → Evaluation → Deployment.  
- Provides business insights into sales trends, seasonality, and holiday effects.  
- Interactive dashboard makes results **easy to interpret for decision-makers**.  
