"""
Sales Analytics System with ML Models and Premium Dashboard
Production-level implementation with modular architecture
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_processor import DataProcessor
from model_manager import ModelManager
from dashboard_components import DashboardComponents
from analytics_engine import AnalyticsEngine

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check if user is on mobile and restrict access
try:
    user_agent = st.context.headers.get('user-agent', '').lower()
except:
    user_agent = ''

mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'tablet']
is_mobile = any(keyword in user_agent for keyword in mobile_keywords)

if is_mobile:
    st.error("🖥️ Desktop Only Access")
    st.markdown("""
    ### This application is optimized for desktop use only.
    
    Please open this dashboard on a desktop or laptop computer for the best experience.
    
    **Why desktop only?**
    - Complex data visualizations
    - Advanced analytics features
    - Better screen real estate
    - Optimal user experience
    """)
    st.stop()

# Custom CSS for enhanced design
st.markdown("""
<style>
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f1419 0%, #1a237e 50%, #3949ab 100%);
        padding: 0;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #3f51b5 0%, #1a237e 100%);
        padding: 2rem 1.5rem;
        margin: -1rem -1rem 0 -1rem;
        border-radius: 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(63, 81, 181, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .sidebar-title {
        color: white;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        letter-spacing: 0.5px;
    }
    
    .sidebar-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    .filter-section {
        margin: 2rem 0;
        position: relative;
    }
    
    .filter-title-header {
        background: linear-gradient(135deg, rgba(63, 81, 181, 0.8) 0%, rgba(26, 35, 126, 0.8) 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px 12px 0 0;
        border: 1px solid rgba(63, 81, 181, 0.3);
        border-bottom: none;
        backdrop-filter: blur(10px);
    }
    
    .filter-title {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    

    
    .sidebar-metric {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #3f51b5;
        transition: all 0.3s ease;
    }
    
    .sidebar-metric:hover {
        background: rgba(255,255,255,0.15);
        transform: translateX(5px);
    }
    
    .sidebar-metric-label {
        color: rgba(255,255,255,0.8);
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sidebar-metric-value {
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Container styling to connect with filter headers */
    .css-1d391kg .filter-section + div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(63, 81, 181, 0.3) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        margin-top: -1px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .css-1d391kg .filter-section + div:hover {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(63, 81, 181, 0.5) !important;
        box-shadow: 0 8px 25px rgba(63, 81, 181, 0.15) !important;
    }
    
    /* Streamlit widget overrides */
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(63, 81, 181, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1d391kg .stSelectbox > div > div:hover {
        border-color: rgba(63, 81, 181, 0.6) !important;
        box-shadow: 0 4px 12px rgba(63, 81, 181, 0.2) !important;
    }
    
    .css-1d391kg .stMultiSelect > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(63, 81, 181, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1d391kg .stMultiSelect > div > div:hover {
        border-color: rgba(63, 81, 181, 0.6) !important;
        box-shadow: 0 4px 12px rgba(63, 81, 181, 0.2) !important;
    }
    
    .css-1d391kg .stDateInput > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(63, 81, 181, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1d391kg .stDateInput > div > div:hover {
        border-color: rgba(63, 81, 181, 0.6) !important;
        box-shadow: 0 4px 12px rgba(63, 81, 181, 0.2) !important;
    }
    
    .css-1d391kg .stExpander {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        margin: 0.8rem 0 !important;
    }
    
    .css-1d391kg .stExpander > div:first-child {
        background: rgba(63, 81, 181, 0.2) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.8rem 1rem !important;
    }
    
    /* Main content styling */
    .main-header {
        background: linear-gradient(135deg, #3f51b5 0%, #1a237e 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(63, 81, 181, 0.3);
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #3f51b5 0%, #1a237e 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.3rem;
        box-shadow: 0 8px 25px rgba(63, 81, 181, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(63, 81, 181, 0.3);
    }
    
    .metric-icon {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
        display: block;
    }
    
    .metric-title {
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        line-height: 1.1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

class SalesAnalyticsDashboard:
    def __init__(self):
        # Use robust path detection for deployment
        import os
        csv_path = "sales_data.csv"
        if not os.path.exists(csv_path):
            # Try alternative paths
            possible_paths = [
                "./sales_data.csv",
                "../sales_data.csv", 
                "/mount/src/mlmodel/sales_data.csv",
                os.path.join(os.path.dirname(__file__), "sales_data.csv")
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    csv_path = path
                    break
        self.data_processor = DataProcessor(csv_path)
        self.model_manager = ModelManager()
        self.dashboard_components = DashboardComponents()
        self.analytics_engine = AnalyticsEngine()
        
    def load_and_process_data(self):
        """Load and process the sales data"""
        if 'processed_data' not in st.session_state:
            with st.spinner("Loading and processing data..."):
                # Debug info
                import os
                st.write(f"Debug: Looking for CSV at: {self.data_processor.filepath}")
                st.write(f"Debug: File exists: {os.path.exists(self.data_processor.filepath)}")
                st.write(f"Debug: Current directory: {os.getcwd()}")
                st.write(f"Debug: Directory contents: {os.listdir('.')}")
                
                # Load data
                if self.data_processor.load_data():
                    # Process data
                    processed_df = self.data_processor.preprocess_data()
                    if processed_df is not None and not processed_df.empty:
                        st.session_state.processed_data = processed_df
                        st.session_state.eda_summary = self.data_processor.get_eda_summary()
                        return True
                    else:
                        st.error("No data loaded. Please check if the CSV file exists and is readable.")
                        return False
                else:
                    st.error("No data loaded. Please check if the CSV file exists and is readable.")
                    return False
        return True
    
    def train_models(self, force_retrain=False):
        """Train ML models for profit prediction"""
        if not force_retrain and 'models_trained' in st.session_state and st.session_state.models_trained:
            return True
            
        with st.spinner("Training ML models..."):
            # Ensure data is loaded first
            if self.data_processor.df is None:
                if not self.data_processor.load_data():
                    st.error("No data loaded. Please check if the CSV file exists and is readable.")
                    return False
                self.data_processor.preprocess_data()
                
            X, y = self.data_processor.prepare_model_data(target='TOTAL_PROFIT')
            if X is not None and y is not None:
                results = self.model_manager.train_models(X, y, test_size=0.2)
                st.session_state.model_results = results
                st.session_state.models_trained = True
                st.session_state.trained_model_manager = self.model_manager
                return True
            else:
                st.error("Failed to prepare model data")
                return False
    
    def render_sidebar(self):
        """Render enhanced sidebar with expert UI/UX design"""
        # Sidebar Header
        st.sidebar.markdown("""
        <div class="sidebar-header">
            <h2 class="sidebar-title">🎛️ Control Center</h2>
            <p class="sidebar-subtitle">Advanced Analytics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if data is loaded
        if 'processed_data' not in st.session_state:
            st.sidebar.error("No data loaded. Please check if the CSV file exists and is readable.")
            return None
            
        df = st.session_state.processed_data
        
        # Data Filters Section
        st.sidebar.markdown("""
        <div class="filter-section">
            <div class="filter-title-header">
                <div class="filter-title">📊 Data Filters</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.sidebar.container():
            # Date range filter
            with st.expander("📅 Date Range", expanded=True):
                date_range = st.date_input(
                    "Select Period",
                    value=(df['ORDERDATE'].min(), df['ORDERDATE'].max()),
                    min_value=df['ORDERDATE'].min(),
                    max_value=df['ORDERDATE'].max()
                )
            
            # Product line filter
            with st.expander("🏷️ Product Lines", expanded=False):
                product_lines = st.multiselect(
                    "Choose Products",
                    options=df['PRODUCTLINE'].unique().tolist(),
                    default=df['PRODUCTLINE'].unique().tolist()
                )
            
            # Territory filter
            with st.expander("🌍 Territories", expanded=False):
                territories = st.multiselect(
                    "Select Regions",
                    options=df['TERRITORY'].unique().tolist(),
                    default=df['TERRITORY'].unique().tolist()
                )
            
            # Deal size filter
            with st.expander("💼 Deal Sizes", expanded=False):
                deal_sizes = st.multiselect(
                    "Filter by Size",
                    options=df['DEALSIZE'].unique().tolist(),
                    default=df['DEALSIZE'].unique().tolist()
                )
            
            # Customer segment filter
            with st.expander("👥 Customer Segments", expanded=False):
                customer_segments = st.multiselect(
                    "Select Segments",
                    options=df['CUSTOMER_SEGMENT'].unique().tolist(),
                    default=df['CUSTOMER_SEGMENT'].unique().tolist()
                )
        
        # Apply filters
        filtered_df = df[
            (df['ORDERDATE'] >= pd.to_datetime(date_range[0])) &
            (df['ORDERDATE'] <= pd.to_datetime(date_range[1])) &
            (df['PRODUCTLINE'].isin(product_lines)) &
            (df['TERRITORY'].isin(territories)) &
            (df['DEALSIZE'].isin(deal_sizes)) &
            (df['CUSTOMER_SEGMENT'].isin(customer_segments))
        ]
        
        st.session_state.filtered_data = filtered_df
        
        # ML Model Controls Section
        st.sidebar.markdown("""
        <div class="filter-section">
            <div class="filter-title-header">
                <div class="filter-title">🤖 AI & Analytics</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.sidebar.container():
            model_action = st.selectbox(
                "🔬 Model Operations",
                ["View Performance", "Make Predictions", "Feature Importance", "Hyperparameter Tuning"],
                help="Select an AI model operation to perform"
            )
            
            if st.button("🔄 Retrain Models", help="Force retrain all models"):
                st.session_state.models_trained = False
                self.train_models(force_retrain=True)
                st.success("Models retrained successfully!")
        
        # Quick Stats
        st.sidebar.markdown("""
        <div class="filter-section">
            <div class="filter-title-header">
                <div class="filter-title">📈 Quick Stats</div>
            </div>
            <div class="filter-content">
                <div class="sidebar-metric">
                    <div class="sidebar-metric-label">Filtered Records</div>
                    <div class="sidebar-metric-value">{:,}</div>
                </div>
                <div class="sidebar-metric">
                    <div class="sidebar-metric-label">Total Revenue</div>
                    <div class="sidebar-metric-value">${:,.0f}</div>
                </div>
                <div class="sidebar-metric">
                    <div class="sidebar-metric-label">Avg Order Value</div>
                    <div class="sidebar-metric-value">${:,.0f}</div>
                </div>
            </div>
        </div>
        """.format(
            len(filtered_df),
            filtered_df['SALES'].sum(),
            filtered_df['SALES'].mean()
        ), unsafe_allow_html=True)
        
        return model_action
    
    def render_main_dashboard(self):
        """Render main dashboard content"""
        # Enhanced Header
        st.markdown("""
        <div class="main-header">
            <h1 class="header-title">Sales Analytics Dashboard</h1>
            <p class="header-subtitle">Advanced Business Intelligence & Machine Learning Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if data is loaded
        if 'processed_data' not in st.session_state:
            st.error("No data loaded. Please check if the CSV file exists and is readable.")
            return
            
        if 'filtered_data' not in st.session_state:
            st.error("No filtered data available. Please check the sidebar filters.")
            return
            
        df = st.session_state.filtered_data
        
        # KPI Section
        self.render_kpi_section(df)
        
        # Charts Section
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_sales_trend_chart(df)
            self.render_product_performance_chart(df)
        
        with col2:
            self.render_territory_analysis_chart(df)
            self.render_customer_analysis_chart(df)
        
        # Detailed Analytics
        self.render_detailed_analytics(df)
    
    def render_kpi_section(self, df):
        """Render enhanced KPI metrics section"""
        
        # Calculate metrics
        total_sales = df['SALES'].sum()
        total_orders = len(df)
        avg_order_value = df['SALES'].mean()
        total_customers = df['CUSTOMERNAME'].nunique()
        total_profit = df['TOTAL_PROFIT'].sum() if 'TOTAL_PROFIT' in df.columns else 0
        
        # Create columns with equal spacing
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">💰</span>
                <div class="metric-title">Total Sales</div>
                <h2 class="metric-value">${total_sales:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">📦</span>
                <div class="metric-title">Total Orders</div>
                <h2 class="metric-value">{total_orders:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">💵</span>
                <div class="metric-title">Avg Order Value</div>
                <h2 class="metric-value">${avg_order_value:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">👥</span>
                <div class="metric-title">Total Customers</div>
                <h2 class="metric-value">{total_customers:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">💎</span>
                <div class="metric-title">Total Profit</div>
                <h2 class="metric-value">${total_profit:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Add bottom padding
        st.markdown("<div style='padding-bottom: 3rem;'></div>", unsafe_allow_html=True)
    
    def render_sales_trend_chart(self, df):
        """Render sales trend over time"""
        st.markdown("### 📊 Sales Trend Analysis")
        
        # Monthly sales trend
        monthly_sales = df.groupby(df['ORDERDATE'].dt.to_period('M'))['SALES'].sum().reset_index()
        monthly_sales['ORDERDATE'] = monthly_sales['ORDERDATE'].astype(str)
        
        fig = px.line(
            monthly_sales, 
            x='ORDERDATE', 
            y='SALES',
            title="Monthly Sales Trend",
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        fig.update_traces(line_color='#00E676')
        st.plotly_chart(fig, use_container_width=True)
    
    def render_product_performance_chart(self, df):
        """Render product line performance"""
        st.markdown("### 🏷️ Product Performance")
        
        product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=True).reset_index()
        
        fig = px.bar(
            product_sales,
            x='SALES',
            y='PRODUCTLINE',
            orientation='h',
            title="Sales by Product Line",
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        fig.update_traces(marker_color='#FF6B35')
        st.plotly_chart(fig, use_container_width=True)
    
    def render_territory_analysis_chart(self, df):
        """Render territory analysis"""
        st.markdown("### 🌍 Territory Analysis")
        
        territory_sales = df.groupby('TERRITORY')['SALES'].sum()
        
        fig = px.pie(
            values=territory_sales.values,
            names=territory_sales.index,
            title="Sales Distribution by Territory",
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        fig.update_traces(marker=dict(colors=['#9C27B0', "#E6E91E", '#F44336', '#FF9800', '#4CAF50']))
        st.plotly_chart(fig, use_container_width=True)
    
    def render_customer_analysis_chart(self, df):
        """Render customer segment analysis"""
        st.markdown("### 👥 Customer Segment Analysis")
        
        segment_sales = df.groupby('CUSTOMER_SEGMENT')['SALES'].sum()
        
        fig = px.bar(
            x=segment_sales.index,
            y=segment_sales.values,
            title="Sales by Customer Segment",
            template="plotly_dark",
            labels={'x': 'Customer Segment', 'y': 'Sales ($)'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title='Customer Segment',
            yaxis_title='Sales ($)'
        )
        fig.update_traces(marker_color='#00BCD4')
        st.plotly_chart(fig, use_container_width=True)
    
    def render_detailed_analytics(self, df):
        """Render detailed analytics section"""
        st.markdown("## 🔍 Detailed Analytics")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Sales Analysis", "🎯 Customer Insights", "📦 Product Insights", "📈 Trend Analysis"])
        
        with tab1:
            self.render_sales_analysis(df)
        
        with tab2:
            self.render_customer_insights(df)
        
        with tab3:
            self.render_product_insights(df)
        
        with tab4:
            self.render_trend_analysis(df)
    
    def render_sales_analysis(self, df):
        """Render detailed sales analysis"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by deal size
            deal_size_sales = df.groupby('DEALSIZE')['SALES'].sum()
            fig = px.bar(
                x=deal_size_sales.index,
                y=deal_size_sales.values,
                title="Sales by Deal Size",
                template="plotly_dark",
                labels={'x': 'Deal Size', 'y': 'Sales ($)'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Deal Size',
                yaxis_title='Sales ($)'
            )
            fig.update_traces(marker_color='#FFC107')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sales by status
            status_sales = df.groupby('STATUS')['SALES'].sum()
            fig = px.pie(
                values=status_sales.values,
                names=status_sales.index,
                title="Sales by Order Status",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_customer_insights(self, df):
        """Render customer insights"""
        # Top customers
        top_customers = df.groupby('CUSTOMERNAME')['SALES'].sum().nlargest(10)
        
        fig = px.bar(
            x=top_customers.values,
            y=top_customers.index,
            orientation='h',
            title="Top 10 Customers by Sales",
            template="plotly_dark",
            labels={'x': 'Sales ($)', 'y': 'Customer Name'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Sales ($)',
            yaxis_title='Customer Name'
        )
        fig.update_traces(marker_color='#8BC34A')
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer distribution by country
        country_customers = df.groupby('COUNTRY')['CUSTOMERNAME'].nunique().sort_values(ascending=False)
        
        fig = px.bar(
            x=country_customers.index[:10],
            y=country_customers.values[:10],
            title="Top 10 Countries by Customer Count",
            template="plotly_dark",
            labels={'x': 'Country', 'y': 'Customer Count'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Country',
            yaxis_title='Customer Count'
        )
        fig.update_traces(marker_color='#FF5722')
        st.plotly_chart(fig, use_container_width=True)
    
    def render_product_insights(self, df):
        """Render product insights"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Top products by sales
            top_products = df.groupby('PRODUCTCODE')['SALES'].sum().nlargest(10)
            fig = px.bar(
                x=top_products.values,
                y=top_products.index,
                orientation='h',
                title="Top 10 Products by Sales",
                template="plotly_dark",
                labels={'x': 'Sales ($)', 'y': 'Product Code'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Sales ($)',
                yaxis_title='Product Code'
            )
            fig.update_traces(marker_color='#673AB7')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Product quantity vs sales
            product_metrics = df.groupby('PRODUCTCODE').agg({
                'QUANTITYORDERED': 'sum',
                'SALES': 'sum'
            }).reset_index()
            
            fig = px.scatter(
                product_metrics,
                x='QUANTITYORDERED',
                y='SALES',
                title="Product Quantity vs Sales",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_trend_analysis(self, df):
        """Render trend analysis"""
        # Quarterly trends
        quarterly_sales = df.groupby('QTR_ID')['SALES'].sum()
        
        fig = px.line(
            x=quarterly_sales.index,
            y=quarterly_sales.values,
            title="Quarterly Sales Trend",
            template="plotly_dark",
            labels={'x': 'Quarter', 'y': 'Sales ($)'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Quarter',
            yaxis_title='Sales ($)'
        )
        fig.update_traces(line_color='#E91E63')
        st.plotly_chart(fig, use_container_width=True)
        
        # Year-over-year comparison
        yearly_sales = df.groupby('YEAR_ID')['SALES'].sum()
        
        fig = px.bar(
            x=yearly_sales.index,
            y=yearly_sales.values,
            title="Year-over-Year Sales",
            template="plotly_dark",
            labels={'x': 'Year', 'y': 'Sales ($)'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Year',
            yaxis_title='Sales ($)'
        )
        fig.update_traces(marker_color='#009688')
        st.plotly_chart(fig, use_container_width=True)
    
    def render_ml_section(self, model_action):
        """Render ML model section"""
        st.markdown("## 🤖 Machine Learning Models")
        
        if model_action == "View Performance":
            self.render_model_performance()
        elif model_action == "Make Predictions":
            self.render_predictions()
        elif model_action == "Feature Importance":
            self.render_feature_importance()
        elif model_action == "Hyperparameter Tuning":
            self.render_hyperparameter_tuning()
    
    def render_model_performance(self):
        """Render model performance metrics"""
        st.markdown("### 📊 Model Performance Comparison")
        
        if 'models_trained' not in st.session_state or not st.session_state.models_trained:
            st.info("Please train models first using the 'Retrain Models' button in the sidebar.")
            return
            
        try:
            # Use the trained model manager from session state
            if 'trained_model_manager' in st.session_state:
                trained_model = st.session_state.trained_model_manager
                performance_df = trained_model.get_model_summary()
            else:
                performance_df = None
            
            if performance_df is not None and not performance_df.empty:
                st.dataframe(performance_df, use_container_width=True)
                
                perf_chart_df = performance_df.reset_index()
                
                fig = px.bar(
                    perf_chart_df,
                    x='index',
                    y='R2_Score',
                    title="Model Performance Comparison (R² Score)",
                    template="plotly_dark"
                )
                fig.update_xaxes(title="Model")
                fig.update_yaxes(title="R² Score")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No model performance data available.")
        except Exception as e:
            st.error(f"Error loading model performance: {str(e)}")
    
    def render_predictions(self):
        """Render strategic business intelligence interface"""
        st.markdown("### 🎯 Strategic Business Intelligence")
        
        if 'models_trained' not in st.session_state or not st.session_state.models_trained:
            st.info("Please train models first using the 'Retrain Models' button in the sidebar.")
            return
        
        # Get data for analysis
        df = st.session_state.processed_data
        
        # Strategic Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["🏆 Product Strategy", "🌍 Geographic Insights", "🔮 What-If Analysis"])
        
        with tab1:
            self.render_product_strategy(df)
        
        with tab2:
            self.render_geographic_strategy(df)
        
        with tab3:
            self.render_whatif_analysis(df)

    def render_product_strategy(self, df):
        """Product optimization recommendations"""
        st.markdown("#### 🏆 Product Line Optimization")
        
        # Calculate product metrics
        product_metrics = df.groupby('PRODUCTLINE').agg({
            'TOTAL_PROFIT': ['sum', 'mean'],
            'SALES': 'sum'
        }).round(2)
        
        product_metrics.columns = ['Total_Profit', 'Avg_Profit', 'Total_Sales']
        product_metrics['Profit_Margin'] = (product_metrics['Total_Profit'] / product_metrics['Total_Sales'] * 100).round(2)
        product_metrics = product_metrics.sort_values('Total_Profit', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Best performing product
            best_product = product_metrics.index[0]
            best_profit = product_metrics.iloc[0]['Total_Profit']
            st.success(f"🥇 **Top Performer**: {best_product}")
            st.metric("Total Profit", f"${best_profit:,.0f}")
            
            st.markdown("**💡 Recommendations:**")
            st.write(f"• Focus marketing on {best_product}")
            st.write(f"• Increase {best_product} inventory")
        
        with col2:
            # Growth opportunity
            if len(product_metrics) > 1:
                growth_product = product_metrics.index[1]
                st.info(f"📈 **Growth Opportunity**: {growth_product}")
                st.write(f"• Expand {growth_product} market")
                st.write(f"• Optimize {growth_product} pricing")
        
        # Product performance table
        st.dataframe(product_metrics, use_container_width=True)
    
    def render_geographic_strategy(self, df):
        """Geographic expansion insights"""
        st.markdown("#### 🌍 Geographic Strategy")
        
        # Territory analysis
        territory_metrics = df.groupby('TERRITORY').agg({
            'TOTAL_PROFIT': 'sum',
            'SALES': 'sum'
        }).round(2)
        territory_metrics = territory_metrics.sort_values('TOTAL_PROFIT', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            best_territory = territory_metrics.index[0]
            st.success(f"🌟 **Top Territory**: {best_territory}")
            st.metric("Total Profit", f"${territory_metrics.iloc[0]['TOTAL_PROFIT']:,.0f}")
        
        with col2:
            if len(territory_metrics) > 1:
                growth_territory = territory_metrics.index[1]
                st.info(f"📈 **Expansion Target**: {growth_territory}")
        
        # Territory chart
        fig = px.bar(
            territory_metrics.reset_index(),
            x='TERRITORY',
            y='TOTAL_PROFIT',
            title="Profit by Territory",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_whatif_analysis(self, df):
        """What-if scenario analysis"""
        st.markdown("#### 🔮 Scenario Analysis")
        
        scenario = st.selectbox("Choose Scenario:", [
            "Increase best product by 20%",
            "Focus on large deals",
            "Expand top territory"
        ])
        
        if st.button("Calculate Impact"):
            if "best product" in scenario:
                best_product = df.groupby('PRODUCTLINE')['TOTAL_PROFIT'].sum().idxmax()
                current_profit = df[df['PRODUCTLINE'] == best_product]['TOTAL_PROFIT'].sum()
                impact = current_profit * 0.20
                
                st.success(f"📈 Impact: +${impact:,.0f} profit")
                st.info(f"Focus on {best_product} for maximum return")
        
        # Quick calculator
        st.markdown("#### 🧮 Quick Profit Prediction")
        with st.form("quick_calc"):
            col1, col2 = st.columns(2)
            with col1:
                product = st.selectbox("Product", df['PRODUCTLINE'].unique())
                quantity = st.number_input("Quantity", value=50)
            with col2:
                territory = st.selectbox("Territory", df['TERRITORY'].unique())
                price = st.number_input("Price", value=100.0)
            
            if st.form_submit_button("Calculate"):
                # Estimate based on historical data
                similar = df[(df['PRODUCTLINE'] == product) & (df['TERRITORY'] == territory)]
                if not similar.empty:
                    avg_margin = similar['TOTAL_PROFIT'].sum() / similar['SALES'].sum()
                    estimated_profit = quantity * price * avg_margin
                    st.success(f"💰 Estimated Profit: ${estimated_profit:,.2f}")
    
    def render_feature_importance(self):
        """Render feature importance analysis"""
        st.markdown("### 🎯 Feature Importance Analysis")
        
        if 'models_trained' not in st.session_state or not st.session_state.models_trained:
            st.info("Please train models first using the 'Retrain Models' button in the sidebar.")
            return
            
        # Use the trained model manager from session state
        if 'trained_model_manager' in st.session_state:
            trained_model = st.session_state.trained_model_manager
            feature_cols = self.data_processor.get_feature_columns()
            importance_df = trained_model.get_feature_importance(feature_cols)
        else:
            importance_df = None
        
        if importance_df is not None and not importance_df.empty:
            # Sort by importance for better visualization
            importance_df = importance_df.sort_values('Importance', ascending=True)
            
            fig = px.bar(
                importance_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title="Feature Importance (Best Model)",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Feature importance not available for the current model")
    
    def render_hyperparameter_tuning(self):
        """Render hyperparameter tuning interface"""
        st.markdown("### ⚙️ Hyperparameter Tuning")
        
        if 'models_trained' not in st.session_state or not st.session_state.models_trained:
            st.info("Please train models first using the 'Retrain Models' button in the sidebar.")
            return
            
        model_choice = st.selectbox(
            "Select Model for Tuning",
            ["Random Forest", "XGBoost", "LightGBM"]
        )
        
        if st.button("Start Hyperparameter Tuning"):
            with st.spinner(f"Tuning {model_choice} hyperparameters..."):
                # Ensure data is loaded
                if self.data_processor.df is None:
                    if not self.data_processor.load_data():
                        st.error("No data loaded. Please check if the CSV file exists and is readable.")
                        return
                    self.data_processor.preprocess_data()
                
                X, y = self.data_processor.prepare_model_data(target='TOTAL_PROFIT')
                if X is not None and y is not None:
                    # Use trained model manager if available
                    if 'trained_model_manager' in st.session_state:
                        trained_model = st.session_state.trained_model_manager
                        best_model = trained_model.hyperparameter_tuning(X, y, model_choice)
                    else:
                        best_model = self.model_manager.hyperparameter_tuning(X, y, model_choice)
                    
                    if best_model:
                        st.success("Hyperparameter tuning completed!")
                        st.info("Best model has been updated in the model manager")
                    else:
                        st.error("Hyperparameter tuning failed")
                else:
                    st.error("Failed to prepare model data for hyperparameter tuning")
    
    def run(self):
        """Main application runner"""
        # Load and process data
        if not self.load_and_process_data():
            st.stop()
        
        # Render sidebar and get model action
        model_action = self.render_sidebar()
        
        # Only proceed if sidebar rendered successfully (data is loaded)
        if model_action is not None:
            # Main dashboard
            self.render_main_dashboard()
            
            # ML section
            self.render_ml_section(model_action)
        else:
            st.error("Unable to load dashboard. Please check if the CSV file exists and is readable.")

if __name__ == "__main__":
    # Initialize and run the dashboard
    dashboard = SalesAnalyticsDashboard()
    dashboard.run()