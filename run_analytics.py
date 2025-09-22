#!/usr/bin/env python3
"""
Simple Analytics Runner - No Streamlit Required
"""

import pandas as pd
import numpy as np
from data_processor import DataProcessor
from model_manager import ModelManager
from analytics_engine import AnalyticsEngine

def main():
    print("🚀 Starting Sales Analytics...")
    
    # Initialize components
    data_processor = DataProcessor("d:/New folder (15)/sales_data.csv")
    model_manager = ModelManager()
    analytics_engine = AnalyticsEngine()
    
    # Load and process data
    print("📊 Loading data...")
    if data_processor.load_data():
        print("✅ Data loaded successfully")
        
        # Process data
        print("🔄 Processing data...")
        processed_df = data_processor.preprocess_data()
        print(f"✅ Data processed: {len(processed_df)} rows, {len(processed_df.columns)} columns")
        
        # Display basic statistics
        print("\n📈 Basic Statistics:")
        print(f"Total Sales: ${processed_df['SALES'].sum():,.2f}")
        print(f"Total Orders: {len(processed_df):,}")
        print(f"Average Order Value: ${processed_df['SALES'].mean():,.2f}")
        print(f"Unique Customers: {processed_df['CUSTOMERNAME'].nunique():,}")
        if 'TOTAL_PROFIT' in processed_df.columns:
            print(f"Total Profit: ${processed_df['TOTAL_PROFIT'].sum():,.2f}")
        
        # Train models
        print("\n🤖 Training ML models...")
        X, y = data_processor.prepare_model_data(target='TOTAL_PROFIT')
        if X is not None and y is not None:
            results = model_manager.train_models(X, y, test_size=0.2)
            print("✅ Models trained successfully")
            
            # Display model results
            print("\n🎯 Model Performance:")
            for model_name, metrics in results.items():
                if isinstance(metrics, dict) and 'r2_score' in metrics:
                    print(f"{model_name}: R² = {metrics['r2_score']:.4f}")
        else:
            print("❌ Failed to prepare model data")
    else:
        print("❌ Failed to load data")

if __name__ == "__main__":
    main()