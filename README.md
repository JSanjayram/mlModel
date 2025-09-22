# Sales Analytics Dashboard

A comprehensive sales analytics dashboard built with Streamlit, featuring advanced data visualization, machine learning models, and business intelligence capabilities. This project analyzes sales data to provide actionable insights for business decision-making through interactive visualizations and predictive modeling.

## 🚀 Features

- **Interactive Dashboard**: Modern, responsive UI with professional indigo/blue theme
- **Advanced Analytics**: Comprehensive sales analysis with KPI tracking
- **Machine Learning**: Multiple ML models (Random Forest, XGBoost, LightGBM) for profit prediction
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Filtering System**: Advanced filtering by date, product, territory, and customer segments
- **Mobile Responsive**: Optimized for both desktop and mobile devices
- **Real-time Insights**: Dynamic data processing and visualization

## 📊 Dashboard Components

### Main Features
- **KPI Metrics**: Total sales, orders, average order value, customers, and profit
- **Sales Trends**: Time-series analysis with monthly/quarterly trends
- **Product Performance**: Analysis by product lines and categories
- **Territory Analysis**: Geographic sales distribution
- **Customer Insights**: Customer segmentation and behavior analysis

### Machine Learning Models
- **Profit Prediction**: Advanced ML models for profit forecasting
- **Feature Importance**: Analysis of key factors affecting sales
- **Model Comparison**: Performance metrics for different algorithms
- **Hyperparameter Tuning**: Automated model optimization

## 🔍 What We Analyzed

### Business Intelligence Insights
- **Sales Performance**: Monthly and quarterly sales trends to identify seasonal patterns
- **Product Analysis**: Best-performing product lines and revenue drivers
- **Geographic Distribution**: Territory-wise sales performance and market penetration
- **Customer Segmentation**: Customer behavior patterns and high-value segments
- **Deal Size Impact**: Analysis of small, medium, and large deal contributions
- **Profit Margins**: Product-wise profitability analysis

### Key Metrics Tracked
- Total Sales Revenue
- Order Volume and Frequency
- Average Order Value (AOV)
- Customer Acquisition and Retention
- Profit Margins by Product/Territory
- Sales Growth Rates

## 🤖 Machine Learning Models Comparison

### Why We Use Multiple Models
We implement three different machine learning algorithms to ensure robust predictions and compare their effectiveness:

### 1. Random Forest
- **Purpose**: Ensemble learning for stable predictions
- **Strengths**: Handles non-linear relationships, reduces overfitting
- **Use Case**: Baseline model for profit prediction
- **Performance**: Good interpretability with feature importance

### 2. XGBoost (Extreme Gradient Boosting)
- **Purpose**: Advanced gradient boosting for high accuracy
- **Strengths**: Excellent performance on structured data, handles missing values
- **Use Case**: High-accuracy profit forecasting
- **Performance**: Often achieves best R² scores

### 3. LightGBM (Light Gradient Boosting Machine)
- **Purpose**: Fast and efficient gradient boosting
- **Strengths**: Faster training, lower memory usage, good accuracy
- **Use Case**: Quick model training and deployment
- **Performance**: Balance between speed and accuracy

### Model Selection Process
1. **Training**: All models trained on same dataset
2. **Evaluation**: Compared using R² score, MAE, and RMSE
3. **Validation**: Cross-validation to ensure generalization
4. **Selection**: Best performing model used for predictions

## 📈 Analysis for Visitors & Clients

### For Business Visitors
- **Executive Dashboard**: High-level KPIs and trends at a glance
- **Strategic Insights**: Product and territory performance analysis
- **Growth Opportunities**: Data-driven recommendations for expansion
- **Risk Assessment**: Identification of underperforming segments

### For Data Analysts
- **Detailed Analytics**: Deep-dive into sales patterns and correlations
- **Model Performance**: ML model comparison and feature importance
- **Data Quality**: Comprehensive data preprocessing and validation
- **Predictive Analytics**: Profit forecasting and scenario analysis

### For Sales Teams
- **Territory Analysis**: Geographic performance and opportunities
- **Customer Insights**: High-value customer identification
- **Product Focus**: Best-selling products and profit drivers
- **Deal Size Strategy**: Optimal deal size targeting

### Interactive Features
- **Real-time Filtering**: Dynamic data exploration by date, product, territory
- **What-if Analysis**: Scenario planning for business decisions
- **Drill-down Capabilities**: From high-level metrics to detailed analysis
- **Export Options**: Data and insights export for further analysis

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express, Plotly Graph Objects
- **Machine Learning**: Scikit-learn, XGBoost, LightGBM
- **Styling**: Custom CSS with modern design principles

## 📁 Project Structure

```
sales-analytics-dashboard/
├── main.py                 # Main Streamlit application
├── data_processor.py       # Data loading and preprocessing
├── model_manager.py        # ML model management
├── dashboard_components.py # UI components
├── analytics_engine.py     # Analytics calculations
├── requirements.txt        # Python dependencies
├── sales_data.csv         # Sample sales data
├── run_streamlit.bat      # Windows batch file to run app
└── README.md              # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sales-analytics-dashboard.git
   cd sales-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

   Or on Windows, double-click `run_streamlit.bat`

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📈 Usage

### Data Loading
- Place your CSV file in the project directory
- Update the file path in `main.py` if needed
- The system supports multiple encodings (UTF-8, Latin-1, CP1252)

### Dashboard Navigation
1. **Sidebar Controls**: Use filters to customize data views
2. **KPI Section**: Monitor key performance indicators
3. **Charts**: Interactive visualizations with hover details
4. **ML Models**: Train models and make predictions

### Machine Learning Features
- **Model Training**: Click "Retrain Models" to update ML models
- **Predictions**: Input custom values for profit forecasting
- **Feature Analysis**: Understand which factors drive sales
- **Performance Metrics**: Compare model accuracy and performance

## 🎨 Design Features

- **Modern UI**: Professional indigo/blue gradient theme
- **Responsive Design**: Optimized for all screen sizes
- **Interactive Elements**: Hover effects and smooth animations
- **Dark Theme**: Consistent dark theme throughout
- **Premium Styling**: Glass-morphism effects and modern typography

## 📊 Data Requirements

The dashboard expects CSV data with the following columns:
- `ORDERNUMBER`: Unique order identifier
- `QUANTITYORDERED`: Number of items ordered
- `PRICEEACH`: Price per item
- `SALES`: Total sales amount
- `ORDERDATE`: Order date
- `PRODUCTLINE`: Product category
- `TERRITORY`: Sales territory
- `CUSTOMERNAME`: Customer name
- `DEALSIZE`: Deal size category
- Additional columns for enhanced analysis

## 🔧 Configuration

### Customization Options
- **Colors**: Modify CSS variables in `main.py`
- **Models**: Add new ML models in `model_manager.py`
- **Charts**: Customize visualizations in dashboard methods
- **Filters**: Add new filter options in sidebar

### Performance Optimization
- **Caching**: Streamlit caching for data processing
- **Lazy Loading**: Models trained only when needed
- **Efficient Processing**: Optimized pandas operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- Scikit-learn community for ML tools
- Open source contributors

## 📞 Support

For support, email your-email@example.com or create an issue in the GitHub repository.

---

**Built with ❤️ using Streamlit and Python**
