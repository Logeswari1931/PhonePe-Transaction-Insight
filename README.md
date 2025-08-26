# 📱 PhonePe Transaction Analysis Dashboard  

An interactive data analytics dashboard built with **Streamlit, Plotly, and MySQL** to explore and analyze digital payment trends across India using **PhonePe Pulse data**.  

This project provides real-time insights into transactions, user behavior, insurance adoption, and market growth with advanced visualizations and business case studies.  

---

## 🚀 Features  

- **📊 Interactive Dashboard** – Real-time KPIs and charts.  
- **🗺️ Geographic Analysis** – State-wise heatmaps for transactions, users, and insurance.  
- **👥 User Growth Insights** – Track registered users, device preferences, and engagement metrics.  
- **🛡️ Insurance Market Analytics** – Growth patterns and regional coverage.  
- **🎯 Business Case Studies** – Predefined case studies for strategic insights (e.g., market expansion, payment trends).  
- **💡 Advanced Visuals** – Choropleth maps, pie charts, bar charts, and trend lines with Plotly.  

---

## 🛠️ Tech Stack  

- **Frontend / Dashboard**: [Streamlit](https://streamlit.io/)  
- **Visualization**: [Plotly](https://plotly.com/), [Plotly Graph Objects]  
- **Backend / Database**: MySQL (SQLAlchemy connector)  
- **Data Processing**: Pandas, GeoJSON  

---

## 📂 Project Structure  

```
📁 PhonePe-Dashboard
│── 📄 Main_Streamlit.py   # Main Streamlit dashboard app
│── 📄 app_log.ipynb                # Log notebook for analysis/testing
│── 📄 pysql.ipynb                  # SQL queries and DB integration
│── 📄 README.md                    # Project documentation
```

---

## ⚙️ Setup & Installation  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/phonepe-dashboard.git
   cd phonepe-dashboard
   ```

2. **Install dependencies**  
   ```
   streamlit
   pandas
   plotly
   mysql-connector-python
   SQLAlchemy
   ```

3. **Setup MySQL Database**  
   - Create a database `Project_1`  
   - Import PhonePe Pulse data into tables:  
     - `aggregated_transaction`, `aggregated_user`, `aggregated_insurance`  
     - `map_transaction`, `map_user`, `map_insurance`  
     - `top_transaction`, `top_user`, `top_insurance`  

   Update connection string in `Main_Streamlit.py` if needed:  
   ```python
   engine = create_engine("mysql+mysqlconnector://root:12345@localhost:3306/Project_1")
   ```

4. **Run the Streamlit App**  
   ```bash
   streamlit run Main_Streamlit.py
   ```

5. Open your browser at `http://localhost:8501`

---

### Case Studies  
- Transaction Dynamics  
- User Device & Engagement  
- Insurance Analytics  
- Market Expansion Strategy  
- User Growth Analysis  

---

## 📊 Data Source  

- [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)  

---

## 📌 Future Enhancements  

- Add predictive analytics (ML models for transaction forecasting).  
- Enable drill-down to district-level insights.  
- Deploy on **Streamlit Cloud / AWS / Heroku**.  
- Add authentication for secure access.  

---

## 🤝 Contributing  

Contributions are welcome! Fork the repo and create a pull request.  

---

## 📝 License  

This project is licensed under the **MIT License**.  
