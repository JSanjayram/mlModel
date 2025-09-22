#!/usr/bin/env python3

from data_processor import DataProcessor

# Test data loading
print("Testing data loading...")
data_processor = DataProcessor("d:/New folder (15)/sales_data.csv")

if data_processor.load_data():
    print("[SUCCESS] Data loaded successfully!")
    
    # Test preprocessing
    processed_df = data_processor.preprocess_data()
    if processed_df is not None:
        print("[SUCCESS] Data preprocessed successfully!")
        print(f"Shape: {processed_df.shape}")
        print(f"Columns: {list(processed_df.columns)}")
        
        # Test model data preparation
        X, y = data_processor.prepare_model_data(target='TOTAL_PROFIT')
        if X is not None and y is not None:
            print("[SUCCESS] Model data prepared successfully!")
            print(f"Features shape: {X.shape}")
            print(f"Target shape: {y.shape}")
        else:
            print("[ERROR] Failed to prepare model data")
    else:
        print("[ERROR] Failed to preprocess data")
else:
    print("[ERROR] Failed to load data")