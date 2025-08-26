# PhonePe Transaction Analysis Dashboard
# Improved layout using only Streamlit components (NO CSS)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import json
import requests

# ========================
# CONFIGURATION
# ========================
st.set_page_config(
    page_title="PhonePe Transaction Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📱"
)

# ========================
# DATABASE CONNECTION
# ========================
@st.cache_resource
def get_database_engine():
    """Create database connection with error handling."""
    try:
        engine = create_engine("mysql+mysqlconnector://root:12345@localhost:3306/Project_1")
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# ========================
# DATA LOADING FUNCTIONS
# ========================

get_state="""select distinct(states) from aggregated_transaction order by states asc;"""
engine = get_database_engine()
df_case_1 = pd.read_sql(get_state, engine)
state_value=df_case_1.values
url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
data_map=json.loads(response.text)
geo_list=[]
for j in data_map["features"]:
    geo_list.append(j["properties"]["ST_NM"])

state_mapping={}
geo_list_sorted=geo_list.sort()
for i in range(len(state_value)):
    state_str=state_value[i][0]
    state_mapping[state_str]=geo_list[i]

url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
geojson_data = json.loads(requests.get(url).text)

@st.cache_data
def load_table_data(table_name):
    """Load data from database table with state name standardization."""
    engine = get_database_engine()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        
        # Standardize state names if States column exists
        
        return df
    except Exception as e:
        st.error(f"Failed to load data from {table_name}: {e}")
        return pd.DataFrame()

# ========================
# DATA LOADING
# ========================
@st.cache_data
def load_all_data():
    """Load all required data tables."""
    tables = {
        "agg_transaction": "aggregated_transaction",
        "agg_insurance": "aggregated_insurance", 
        "agg_user": "aggregated_user",
        "map_transaction": "map_transaction",
        "map_insurance": "map_insurance",
        "map_user": "map_user",
        "top_transaction": "top_transaction",
        "top_insurance": "top_insurance",
        "top_user": "top_user"
    }
    
    data = {}
    for key, table_name in tables.items():
        data[key] = load_table_data(table_name)
    
    return data

# ========================
# VISUALIZATION FUNCTIONS
# ========================
def create_choropleth_map(df, value_col, title, color_scale="Viridis", value_suffix=""):
    """Create a standardized choropleth map."""

    df['States'] = df['States'].replace(state_mapping)
    fig = px.choropleth(
        df,
        geojson=geojson_data,
        featureidkey='properties.ST_NM',
        locations='States',
        color="Amount_M",
        color_continuous_scale='purples',
        hover_name="States",
        hover_data={
            "States":False,
            "Amount_M": True,
            "Transaction_count": True}
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type='mercator',
        projection_scale=1.2,
        center={"lat": 22.5, "lon": 78.5}
    )

    fig.update_layout(
        width=1600,
        height=650,
        margin=dict(l=100, r=0, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        dragmode=False,
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        coloraxis_showscale=False
    )

    # Show the chart
    st.plotly_chart(fig, use_container_width= True)

def create_pie_chart(df, values_col, names_col, title):
    """Create a standardized pie chart."""
    if df.empty:
        st.warning("No data available for the chart.")
        return None
    
    fig = px.pie(df, values=values_col, names=names_col, title=title, hole=0.4)
    fig.update_layout(height=400)
    return fig

def create_bar_chart(df, x_col, y_col, title, text_auto=True):
    """Create a standardized bar chart."""
    if df.empty:
        st.warning("No data available for the chart.")
        return None
    
    fig = px.bar(df, x=x_col, y=y_col, title=title, text_auto=text_auto, color=x_col)
    fig.update_layout(height=400, xaxis_title=x_col.replace('_', ' ').title(), 
                     yaxis_title=y_col.replace('_', ' ').title())
    return fig

# ========================
# LOAD DATA
# ========================
data = load_all_data()

# ========================
# SIDEBAR NAVIGATION
# ========================
with st.sidebar:
    st.title("📱 PhonePe Analytics")
    
    # Navigation in expander
    with st.expander("🚀 Navigation", expanded=True):
        page = st.radio("Select Section", ["📊 Dashboard", "🔍 Case Studies"], label_visibility="collapsed")
    
    # Quick stats in expander
    with st.expander("📈 Quick Stats", expanded=False):
        if not data["agg_transaction"].empty:
            total_transactions = data["agg_transaction"]["Transaction_count"].sum()
            total_amount = data["agg_transaction"]["Transaction_amount"].sum()
            st.metric("Transactions", f"{total_transactions / 1e9:.1f}B")
            st.metric("Amount", f"₹{total_amount / 1e12:.1f}T")
    
    # Info section
    with st.expander("ℹ️ About", expanded=False):
        st.info("""
        **PhonePe Transaction Dashboard**
        
        📈 Real-time Analytics  
        🗺️ Geographic Analysis  
        📱 User Behavior Metrics  
        🛡️ Insurance Analytics  
        
        **Tech**: Streamlit • Plotly • MySQL
        """)

# ========================
# MAIN DASHBOARD
# ========================
if page == "📊 Dashboard":
    
    # Header section with columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📱 PhonePe Transaction Analytics")
    
    # Welcome message in container
    with st.container():
        st.markdown("""
        ### 🌟 Welcome to PhonePe Analytics Hub
        Comprehensive insights into India's digital payment ecosystem with real-time analytics and business intelligence.
        """)
    
    st.divider()
    
    # Key metrics in 4 columns
    st.subheader("📊 Key Performance Indicators")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        if not data["agg_transaction"].empty:
            total_transactions = data["agg_transaction"]["Transaction_count"].sum()
            st.metric(
                label="💳 Total Transactions",
                value=f"{total_transactions / 1e9:.1f}B",
                delta="Real-time data"
            )
    
    with metric_col2:
        if not data["agg_transaction"].empty:
            total_amount = data["agg_transaction"]["Transaction_amount"].sum()
            st.metric(
                label="💰 Total Amount", 
                value=f"₹{total_amount / 1e12:.1f}T",
                delta="Cumulative"
            )
    
    with metric_col3:
        if not data["top_user"].empty:
            total_users = data["top_user"]["Registered_Users"].sum()
            st.metric(
                label="👥 Registered Users", 
                value=f"{total_users / 1e6:.1f}M",
                delta="Active base"
            )
        
    with metric_col4:
        if not data["agg_insurance"].empty:
            total_insurance = data["agg_insurance"]["Insurance_amount"].sum()
            st.metric(
                label="🛡️ Insurance Amount", 
                value=f"₹{total_insurance / 1e9:.1f}B",
                delta="Growth sector"
            )
    
    st.divider()
    
    # Main analytics section
    st.subheader("📈 Interactive Analytics")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["🗺️ Geographic View", "📊 Trends", "🔍 Detailed Analysis"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Transaction Heatmap")
            if not data["agg_transaction"].empty:
                latest_year = data["agg_transaction"]["Years"].max()
                latest_quarter = data["agg_transaction"][data["agg_transaction"]["Years"] == latest_year]["Quarter"].max()
                
                filtered_df = data["agg_transaction"][
                    (data["agg_transaction"]["Years"] == latest_year) & 
                    (data["agg_transaction"]["Quarter"] == latest_quarter)
                ].groupby("States").agg({
                    "Transaction_amount": "sum",
                    "Transaction_count": "sum"
                }).reset_index()
                
                filtered_df["Amount_M"] = filtered_df["Transaction_amount"] / 1e6
                
                fig = create_choropleth_map(
                    filtered_df, 
                    "Amount_M", 
                    f"Transaction Amount - {latest_year} Q{latest_quarter}",
                    "Viridis",
                    "₹M"
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Top Performers")
            if not data["agg_transaction"].empty:
                top_states = filtered_df.nlargest(5, "Transaction_amount")
                for idx, row in top_states.iterrows():
                    st.metric(
                        label=row["States"].title(),
                        value=f"₹{row['Amount_M']:.0f}M",
                        delta=f"{row['Transaction_count']:,} txns"
                    )
    
    with tab2:
        st.markdown("##### Transaction Growth Over Time")
        if not data["agg_transaction"].empty:
            trend_data = data["agg_transaction"].groupby(["Years", "Quarter"])["Transaction_amount"].sum().reset_index()
            trend_data["Period"] = trend_data["Years"].astype(str) + " Q" + trend_data["Quarter"].astype(str)
            
            fig = px.line(
                trend_data, 
                x="Period", 
                y="Transaction_amount",
                title="Transaction Amount Over Time",
                markers=True
            )
            fig.update_layout(
                height=600,
                xaxis_title="Time Period",
                yaxis_title="Transaction Amount (₹)",
                yaxis=dict(tickformat=".2e")
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Filters section
        with st.container():
            st.markdown("##### Analysis Filters")
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                analysis_type = st.selectbox(
                    "Analysis Type",
                    ["Transaction Volume", "User Metrics", "Insurance Data"]
                )
            
            with filter_col2:
                time_period = st.selectbox(
                    "Time Period",
                    ["Latest Quarter", "Year-to-Date", "All Time"]
                )
            
            st.info(f"Showing {analysis_type} for {time_period}")

# ========================
# CASE STUDIES PAGE
# ========================
elif page == "🔍 Case Studies":
    
    # Header
    st.title("🔍 Business Intelligence Case Studies")
    
    # Case study selection in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        case_study = st.selectbox(
            "Select Business Case Study",
            [
                "💳 Transaction Dynamics Analysis",
                "📱 Device Usage & User Engagement", 
                "🛡️ Insurance Market Analysis",
                "🎯 Market Expansion Strategy",
                "👥 User Growth Analysis"
            ]
        )
    
    with col2:
        st.info("💡 Choose a case study to explore detailed business scenarios")
    
    st.divider()

    # Case Study 1: Transaction Dynamics
    if case_study == "💳 Transaction Dynamics Analysis":
        
        # Objective box
        with st.container():
            st.success("""
            **🎯 Objective:** Analyze transaction patterns across states, quarters, and payment types for strategic decision making.
            """)
        
        # Time controls in columns
        st.subheader("⏰ Analysis Controls")
        control_col1, control_col2, control_col3 = st.columns([1, 1, 2])
        
        with control_col1:
            years = sorted(data["agg_transaction"]["Years"].unique()) if not data["agg_transaction"].empty else [2023]
            selected_year = st.selectbox("Year", years, key="td_year")
        
        with control_col2:
            quarters = sorted(data["agg_transaction"][data["agg_transaction"]["Years"] == selected_year]["Quarter"].unique()) if not data["agg_transaction"].empty else [1]
            selected_quarter = st.selectbox("Quarter", quarters, key="td_quarter")
        
        with control_col3:
            st.metric("Analysis Period", f"{selected_year} Q{selected_quarter}")

        if not data["agg_transaction"].empty:
            filtered_data = data["agg_transaction"][
                (data["agg_transaction"]["Years"] == selected_year) & 
                (data["agg_transaction"]["Quarter"] == selected_quarter)
            ]
            
            if not filtered_data.empty:
                # Analysis in tabs
                analysis_tab1, analysis_tab2 = st.tabs(["🗺️ Geographic Analysis", "💼 Payment Types"])
                
                with analysis_tab1:
                    state_summary = filtered_data.groupby("States").agg({
                        "Transaction_amount": "sum",
                        "Transaction_count": "sum"
                    }).reset_index()
                    state_summary["Amount_M"] = state_summary["Transaction_amount"] / 1e6
                    
                    map_col, bar_col = st.columns([3, 2])
                    
                    with map_col:
                        st.markdown("##### State-wise Transaction Heatmap")
                        fig = create_choropleth_map(
                            state_summary, 
                            "Amount_M", 
                            f"Transactions - {selected_year} Q{selected_quarter}",
                            "Blues",
                            "₹M"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with bar_col:
                        st.markdown("##### Top 10 States")
                        top_states = state_summary.nlargest(10, "Transaction_amount")
                        top_states["Amount_B"] = top_states["Transaction_amount"] / 1e9
                        
                        fig = create_bar_chart(
                            top_states, 
                            "States", 
                            "Amount_B", 
                            "Top States (₹B)"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                
                with analysis_tab2:
                    if "Transaction_type" in filtered_data.columns:
                        payment_summary = filtered_data.groupby("Transaction_type")["Transaction_count"].sum().nlargest(5).reset_index()
                        
                        pie_col, insights_col = st.columns([2, 1])
                        
                        with pie_col:
                            st.markdown("##### Payment Method Distribution")
                            fig = create_pie_chart(
                                payment_summary, 
                                "Transaction_count", 
                                "Transaction_type",
                                "Payment Types"
                            )
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with insights_col:
                            st.markdown("##### Key Insights")
                            for idx, row in payment_summary.head(3).iterrows():
                                percentage = (row["Transaction_count"] / payment_summary["Transaction_count"].sum()) * 100
                                st.metric(
                                    label=row["Transaction_type"],
                                    value=f"{percentage:.1f}%",
                                    delta="Market Share"
                                )

    # Case Study 2: Device Usage
    elif case_study == "📱 Device Usage & User Engagement":
        
        with st.container():
            st.success("""
            **🎯 Objective:** Understand user device preferences and engagement patterns to optimize app performance.
            """)
        
        # Controls
        st.subheader("⏰ Analysis Period")
        year_col, quarter_col = st.columns(2)
        
        with year_col:
            years = sorted(data["agg_user"]["Years"].unique()) if not data["agg_user"].empty else [2023]
            selected_year = st.selectbox("Year", years, key="device_year")
        
        with quarter_col:
            quarters = sorted(data["agg_user"][data["agg_user"]["Years"] == selected_year]["Quarter"].unique()) if not data["agg_user"].empty else [1]
            selected_quarter = st.selectbox("Quarter", quarters, key="device_quarter")

        if not data["agg_user"].empty:
            user_data = data["agg_user"][
                (data["agg_user"]["Years"] == selected_year) & 
                (data["agg_user"]["Quarter"] == selected_quarter)
            ]
            
            # Results in columns
            device_col, engagement_col = st.columns(2)
            
            with device_col:
                st.markdown("##### Device Brand Distribution")
                if not user_data.empty and "Brands" in user_data.columns:
                    brand_summary = user_data.groupby("Brands")["Transaction_count"].sum().nlargest(8).reset_index()
                    fig = create_pie_chart(
                        brand_summary, 
                        "Transaction_count", 
                        "Brands",
                        "Device Brands"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            with engagement_col:
                st.markdown("##### Top Districts by App Opens")
                if not data["map_user"].empty:
                    map_user_filtered = data["map_user"][
                        (data["map_user"]["Years"] == selected_year) & 
                        (data["map_user"]["Quarter"] == selected_quarter)
                    ]
                    if not map_user_filtered.empty and "AppOpens" in map_user_filtered.columns:
                        district_opens = map_user_filtered.groupby("District")["AppOpens"].sum().nlargest(10).reset_index()
                        fig = create_bar_chart(
                            district_opens, 
                            "District", 
                            "AppOpens",
                            "App Opens by District"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)

    # Case Study 3: Insurance Analysis
    elif case_study == "🛡️ Insurance Market Analysis":
        
        with st.container():
            st.success("""
            **🎯 Objective:** Analyze insurance transaction growth and identify market expansion opportunities.
            """)
        
        # Controls in expander
        with st.expander("⚙️ Analysis Settings", expanded=True):
            ins_col1, ins_col2 = st.columns(2)
            
            with ins_col1:
                years = sorted(data["agg_insurance"]["Years"].unique()) if not data["agg_insurance"].empty else [2023]
                selected_year = st.selectbox("Year", years, key="ins_year")
            
            with ins_col2:
                quarters = sorted(data["agg_insurance"][data["agg_insurance"]["Years"] == selected_year]["Quarter"].unique()) if not data["agg_insurance"].empty else [1]
                selected_quarter = st.selectbox("Quarter", quarters, key="ins_quarter")

        if not data["agg_insurance"].empty:
            insurance_data = data["agg_insurance"][
                (data["agg_insurance"]["Years"] == selected_year) & 
                (data["agg_insurance"]["Quarter"] == selected_quarter)
            ]
            
            if not insurance_data.empty:
                insurance_summary = insurance_data.groupby("State").agg({
                    "Insurance_amount": "sum",
                    "Insurance_count": "sum"
                }).reset_index()
                insurance_summary["Amount_K"] = insurance_summary["Insurance_amount"] / 1e3
                
                # Side by side analysis
                insurance_col1, insurance_col2 = st.columns(2)
                
                with insurance_col1:
                    st.markdown("##### Insurance Coverage Heatmap")
                    fig = create_choropleth_map(
                        insurance_summary, 
                        "Amount_K", 
                        f"Insurance - {selected_year} Q{selected_quarter}",
                        "Oranges",
                        "₹K"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                with insurance_col2:
                    st.markdown("##### Quarterly Growth Trend")
                    yearly_data = data["agg_insurance"][data["agg_insurance"]["Years"] == selected_year]
                    if not yearly_data.empty:
                        growth_trend = yearly_data.groupby("Quarter")["Insurance_amount"].sum().reset_index()
                        fig = px.line(
                            growth_trend, 
                            x="Quarter", 
                            y="Insurance_amount",
                            title="Insurance Growth",
                            markers=True
                        )
                        fig.update_layout(height=400, yaxis=dict(tickformat=".2e"))
                        st.plotly_chart(fig, use_container_width=True)

    # Case Study 4: Market Expansion
    elif case_study == "🎯 Market Expansion Strategy":
        
        with st.container():
            st.success("""
            **🎯 Objective:** Identify high-potential regions and growth opportunities for market expansion.
            """)
        
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            years = sorted(data["map_transaction"]["Years"].unique()) if not data["map_transaction"].empty else [2023]
            selected_year = st.selectbox("Year", years, key="exp_year")
        
        with exp_col2:
            quarters = sorted(data["map_transaction"][data["map_transaction"]["Years"] == selected_year]["Quarter"].unique()) if not data["map_transaction"].empty else [1]
            selected_quarter = st.selectbox("Quarter", quarters, key="exp_quarter")

        if not data["map_transaction"].empty:
            expansion_data = data["map_transaction"][
                (data["map_transaction"]["Years"] == selected_year) & 
                (data["map_transaction"]["Quarter"] == selected_quarter)
            ]
            
            if not expansion_data.empty:
                expansion_summary = expansion_data.groupby("State").agg({
                    "Transaction_amount": "sum",
                    "Transaction_count": "sum"
                }).reset_index()
                expansion_summary["Amount_M"] = expansion_summary["Transaction_amount"] / 1e6
                
                # Analysis tabs
                market_tab1, market_tab2 = st.tabs(["🗺️ Market Penetration", "📊 Growth Opportunities"])
                
                with market_tab1:
                    st.markdown("##### Market Penetration Heatmap")
                    fig = create_choropleth_map(
                        expansion_summary, 
                        "Amount_M", 
                        f"Market Penetration - {selected_year} Q{selected_quarter}",
                        "Reds",
                        "₹M"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                with market_tab2:
                    st.markdown("##### Growth Potential Analysis")
                    expansion_summary["Growth_Score"] = (
                        expansion_summary["Transaction_amount"] / expansion_summary["Transaction_count"]
                    ).fillna(0)
                    
                    top_growth = expansion_summary.nlargest(10, "Growth_Score")
                    fig = create_bar_chart(
                        top_growth, 
                        "State", 
                        "Growth_Score",
                        "Growth Potential by State"
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

    # Case Study 5: User Growth
    elif case_study == "👥 User Growth Analysis":
        
        with st.container():
            st.success("""
            **🎯 Objective:** Analyze user registration patterns and engagement metrics for growth strategy.
            """)
        
        user_col1, user_col2 = st.columns(2)
        
        with user_col1:
            years = sorted(data["map_user"]["Years"].unique()) if not data["map_user"].empty else [2023]
            selected_year = st.selectbox("Year", years, key="user_year")
        
        with user_col2:
            quarters = sorted(data["map_user"][data["map_user"]["Years"] == selected_year]["Quarter"].unique()) if not data["map_user"].empty else [1]
            selected_quarter = st.selectbox("Quarter", quarters, key="user_quarter")

        if not data["map_user"].empty:
            user_growth_data = data["map_user"][
                (data["map_user"]["Years"] == selected_year) & 
                (data["map_user"]["Quarter"] == selected_quarter)
            ]
            
            if not user_growth_data.empty:
                user_summary = user_growth_data.groupby("State").agg({
                    "RegisteredUsers": "sum",
                    "AppOpens": "sum"
                }).reset_index()
                user_summary["Users_K"] = user_summary["RegisteredUsers"] / 1e3
                
                # User analysis in container
                with st.container():
                    user_analysis_col1, user_analysis_col2 = st.columns(2)
                    
                    with user_analysis_col1:
                        st.markdown("##### User Distribution Heatmap") 
                        fig = create_choropleth_map(
                            user_summary, 
                            "Users_K", 
                            f"Users - {selected_year} Q{selected_quarter}",
                            "Purples",
                            "K Users"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with user_analysis_col2:
                        st.markdown("##### User Engagement Analysis")
                        user_summary["Engagement_Rate"] = (
                            user_summary["AppOpens"] / user_summary["RegisteredUsers"]
                        ).fillna(0)
                        
                        top_engagement = user_summary.nlargest(10, "Engagement_Rate")
                        fig = create_bar_chart(
                            top_engagement, 
                            "State", 
                            "Engagement_Rate",
                            "User Engagement by State"
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)

# ========================
# FOOTER
# ========================
st.divider()
with st.container():
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.info("📊 **Real-time Analytics**\nLive transaction insights")
    
    with footer_col2:
        st.info("🗺️ **Geographic Intelligence**\nState-wise performance metrics")
    
    with footer_col3:
        st.info("🚀 **Business Intelligence**\nData-driven strategic insights")

st.markdown("""
---
**Data Source:** PhonePe Pulse GitHub Repository | **Technology Stack:** Streamlit, Plotly, Pandas, MySQL
""")