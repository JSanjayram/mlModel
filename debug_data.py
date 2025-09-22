#!/usr/bin/env python3
"""
Debug script to check data loading issues
"""

import pandas as pd
import os
from data_processor import DataProcessor

def debug_data_loading():
    filepath = "sales_data.csv"
    
    print("=== Data Loading Debug ===")
    print(f"File path: {filepath}")
    print(f"File exists: {os.path.exists(filepath)}")
    
    if os.path.exists(filepath):
        print(f"File size: {os.path.getsize(filepath)} bytes")
        
        # Try to read first few lines
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                first_lines = [f.readline().strip() for _ in range(3)]
                print("First 3 lines:")
                for i, line in enumerate(first_lines, 1):
                    print(f"  {i}: {line[:100]}...")
        except Exception as e:
            print(f"Error reading file directly: {e}")
        
        # Try DataProcessor
        print("\n=== Testing DataProcessor ===")
        processor = DataProcessor(filepath)
        
        if processor.load_data():
            print(f"✓ Data loaded successfully")
            print(f"  Rows: {len(processor.df)}")
            print(f"  Columns: {len(processor.df.columns)}")
            print(f"  Column names: {list(processor.df.columns)}")
            
            # Test preprocessing
            processed_df = processor.preprocess_data()
            if processed_df is not None:
                print(f"✓ Data preprocessed successfully")
                print(f"  Processed rows: {len(processed_df)}")
                print(f"  Processed columns: {len(processed_df.columns)}")
            else:
                print("✗ Data preprocessing failed")
        else:
            print("✗ Data loading failed")
    else:
        print("✗ File does not exist")

if __name__ == "__main__":
    debug_data_loading()