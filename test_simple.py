#!/usr/bin/env python3
"""
Simple test to verify data loading
"""

from data_processor import DataProcessor

def test_data_loading():
    print("Testing data loading...")
    
    processor = DataProcessor("d:/New folder (15)/sales_data.csv")
    
    # Load data
    if processor.load_data():
        print(f"SUCCESS: Data loaded - {len(processor.df)} rows, {len(processor.df.columns)} columns")
        
        # Process data
        processed_df = processor.preprocess_data()
        if processed_df is not None and not processed_df.empty:
            print(f"SUCCESS: Data processed - {len(processed_df)} rows")
            print("Sample data:")
            print(processed_df.head())
            return True
        else:
            print("ERROR: Data processing failed")
            return False
    else:
        print("ERROR: Data loading failed")
        return False

if __name__ == "__main__":
    test_data_loading()