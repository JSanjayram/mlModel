import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

# Try to import LightGBM, skip if there are compatibility issues
try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("LightGBM not available due to compatibility issues")

class ModelManager:
    def __init__(self):
        self.models = {}
        self.model_performance = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.best_model_name = None
        
    def initialize_models(self):
        """Initialize different ML models for comparison"""
        self.models = {
            'Linear_Regression': LinearRegression(),
            'Random_Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            'Gradient_Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        }
        
        # Add LightGBM only if available
        if LIGHTGBM_AVAILABLE:
            self.models['LightGBM'] = lgb.LGBMRegressor(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
        
    def train_models(self, X, y, test_size=0.2):
        """Train all models and evaluate performance"""
        from sklearn.model_selection import train_test_split
        
        # Initialize models first
        self.initialize_models()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        """Train all models and evaluate performance"""
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model_performance = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            # Train model
            if name in ['XGBoost'] or (name == 'LightGBM' and LIGHTGBM_AVAILABLE):
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            else:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.model_performance[name] = {
                'MSE': mse,
                'RMSE': rmse,
                'MAE': mae,
                'R2_Score': r2,
                'Model': model
            }
            
            print(f"{name} - RMSE: {rmse:.2f}, R2: {r2:.4f}")
        
        # Find best model
        best_r2 = max(self.model_performance.values(), key=lambda x: x['R2_Score'])
        self.best_model_name = [k for k, v in self.model_performance.items() if v['R2_Score'] == best_r2['R2_Score']][0]
        self.best_model = self.model_performance[self.best_model_name]['Model']
        
        print(f"\nBest Model: {self.best_model_name} with R2 Score: {best_r2['R2_Score']:.4f}")
        
        return {
            'performance': self.model_performance,
            'best_model': self.best_model_name,
            'best_score': self.model_performance[self.best_model_name]['R2_Score'] if self.best_model_name else 0
        }
    
    def predict_sales(self, X_new):
        """Make predictions using the best model"""
        if self.best_model is None:
            raise ValueError("No trained model available. Please train models first.")
        
        if self.best_model_name in ['XGBoost'] or (self.best_model_name == 'LightGBM' and LIGHTGBM_AVAILABLE):
            predictions = self.best_model.predict(X_new)
        else:
            X_new_scaled = self.scaler.transform(X_new)
            predictions = self.best_model.predict(X_new_scaled)
        
        return predictions
    
    def predict(self, X_new):
        """Alias for predict_sales to match expected interface"""
        return self.predict_sales(X_new)
    
    def get_feature_importance(self, feature_names):
        """Get feature importance from the best model"""
        if self.best_model is None:
            return None
        
        if hasattr(self.best_model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': self.best_model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            return importance_df
        else:
            return None
    
    def save_model(self, filepath):
        """Save the best model"""
        if self.best_model is None:
            raise ValueError("No trained model to save.")
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'model_name': self.best_model_name,
            'performance': self.model_performance[self.best_model_name]
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a saved model"""
        model_data = joblib.load(filepath)
        self.best_model = model_data['model']
        self.scaler = model_data['scaler']
        self.best_model_name = model_data['model_name']
        
        print(f"Model {self.best_model_name} loaded successfully")
        return model_data['performance']
    
    def predict_future_sales(self, data_processor, months_ahead=6):
        """Predict future sales based on historical trends"""
        df = data_processor.processed_df
        
        # Get the latest date and create future dates
        latest_date = df['ORDERDATE'].max()
        future_dates = pd.date_range(start=latest_date + pd.DateOffset(months=1), 
                                   periods=months_ahead, freq='M')
        
        # Create future data based on historical patterns
        future_predictions = []
        
        for date in future_dates:
            # Use average values from historical data for prediction
            avg_features = df.select_dtypes(include=[np.number]).mean()
            
            # Update date-related features
            avg_features['YEAR'] = date.year
            avg_features['MONTH'] = date.month
            avg_features['DAY'] = date.day
            avg_features['DAYOFWEEK'] = date.dayofweek
            avg_features['QUARTER'] = date.quarter
            avg_features['QTR_ID'] = date.quarter
            avg_features['MONTH_ID'] = date.month
            avg_features['YEAR_ID'] = date.year
            
            # Get features for modeling
            X, _ = data_processor.get_features_for_modeling()
            feature_cols = X.columns
            
            future_row = avg_features[feature_cols].values.reshape(1, -1)
            
            # Make prediction
            predicted_sales = self.predict_sales(future_row)[0]
            
            future_predictions.append({
                'Date': date,
                'Predicted_Sales': predicted_sales,
                'Year': date.year,
                'Month': date.month,
                'Quarter': date.quarter
            })
        
        return pd.DataFrame(future_predictions)
    
    def get_model_comparison(self):
        """Get comparison of all trained models"""
        if not self.model_performance:
            return None
        
        comparison_df = pd.DataFrame(self.model_performance).T
        comparison_df = comparison_df.drop('Model', axis=1)
        comparison_df = comparison_df.round(4)
        
        return comparison_df.sort_values('R2_Score', ascending=False)
    
    def get_model_summary(self):
        """Get summary of model performance"""
        return self.get_model_comparison()
    
    def customer_lifetime_value_prediction(self, customer_data):
        """Predict customer lifetime value"""
        # This is a simplified CLV prediction
        # In practice, you'd want a more sophisticated approach
        
        if self.best_model is None:
            raise ValueError("No trained model available.")
        
        # Use customer metrics to predict future value
        predictions = self.predict_sales(customer_data)
        
        # Multiply by estimated customer lifetime (in orders)
        estimated_lifetime_orders = 10  # This should be calculated based on historical data
        clv_predictions = predictions * estimated_lifetime_orders
        
        return clv_predictions
    
    def hyperparameter_tuning(self, X, y, model_choice):
        # Placeholder: Only Random Forest implemented for simplicity
        if model_choice == "Random Forest":
            from sklearn.model_selection import GridSearchCV
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20]
            }
            rf = RandomForestRegressor(random_state=42)
            grid = GridSearchCV(rf, param_grid, cv=3, scoring='r2')
            grid.fit(X, y)
            self.best_model = grid.best_estimator_
            self.models['Random Forest'] = self.best_model
            return self.best_model
        # Add XGBoost/LightGBM if needed
        return None