import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(self.filepath, encoding=encoding)
                    print(f"Data loaded successfully with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise Exception("Could not decode file with any standard encoding")
            
            # Convert ORDERDATE to datetime if it exists
            if 'ORDERDATE' in self.df.columns:
                self.df['ORDERDATE'] = pd.to_datetime(self.df['ORDERDATE'], errors='coerce')
            
            print(f"Data loaded successfully: {len(self.df)} rows, {len(self.df.columns)} columns")
            print(f"Columns: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def preprocess_data(self):
        if self.df is None:
            print("Error: No data loaded")
            return None
            
        df = self.df.copy()
        
        # Store original df for reference
        self.original_df = self.df.copy()
        
        # Calculate TOTAL_PROFIT if not present
        if 'TOTAL_PROFIT' not in df.columns:
            # Simple profit calculation: Sales minus cost (estimated as QUANTITYORDERED * PRICEEACH * 0.7)
            df['TOTAL_PROFIT'] = df['SALES'] - (df['QUANTITYORDERED'] * df['PRICEEACH'] * 0.7)
        
        # Create CUSTOMER_SEGMENT if not present
        if 'CUSTOMER_SEGMENT' not in df.columns:
            # Segment customers based on sales volume
            df['CUSTOMER_SEGMENT'] = pd.cut(df['SALES'], 
                                          bins=[0, 1000, 5000, float('inf')], 
                                          labels=['Small', 'Medium', 'Large'])
        
        # Encode DEALSIZE
        if 'DEALSIZE' in df.columns:
            deal_size_map = {'Small': 1, 'Medium': 2, 'Large': 3}
            df['DEALSIZE_NUMERIC'] = df['DEALSIZE'].map(deal_size_map).fillna(1)
        
        # Encode STATUS
        if 'STATUS' in df.columns:
            status_map = {k: i+1 for i, k in enumerate(df['STATUS'].unique())}
            df['STATUS_NUMERIC'] = df['STATUS'].map(status_map)
        
        # Encode TERRITORY
        if 'TERRITORY' in df.columns:
            terr_map = {k: i+1 for i, k in enumerate(df['TERRITORY'].unique())}
            df['TERRITORY_RANK'] = df['TERRITORY'].map(terr_map)
        
        # Date features
        if 'ORDERDATE' in df.columns:
            df['YEAR'] = df['ORDERDATE'].dt.year
            df['MONTH'] = df['ORDERDATE'].dt.month
            df['DAY'] = df['ORDERDATE'].dt.day
            df['DAYOFWEEK'] = df['ORDERDATE'].dt.dayofweek
            df['QUARTER'] = df['ORDERDATE'].dt.quarter
        
        # Profit margin
        if 'MSRP' in df.columns and 'PRICEEACH' in df.columns:
            df['PROFIT_MARGIN'] = np.where(df['MSRP'] > 0, (df['PRICEEACH'] - df['MSRP']) / df['MSRP'] * 100, 0)
        
        # Aggregates
        if 'QUANTITYORDERED' in df.columns:
            df['TOTAL_QUANTITY'] = df['QUANTITYORDERED']
            if 'SALES' in df.columns:
                df['AVG_SALES'] = df['SALES'] / df['QUANTITYORDERED']
        
        df['ORDER_COUNT'] = 1
        
        # Drop rows with NaN values in critical columns
        critical_cols = ['SALES', 'QUANTITYORDERED', 'PRICEEACH']
        existing_critical_cols = [col for col in critical_cols if col in df.columns]
        if existing_critical_cols:
            df = df.dropna(subset=existing_critical_cols)
        
        # Store both processed and original data
        self.processed_df = df
        self.df = df  # Keep this for backward compatibility
        
        print(f"Data preprocessed successfully: {len(df)} rows, {len(df.columns)} columns")
        return df

    def get_eda_summary(self):
        df = self.df
        summary = {
            "describe": df.describe(include='all').to_dict(),
            "nulls": df.isnull().sum().to_dict(),
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
        return summary

    def prepare_model_data(self, target='TOTAL_PROFIT'):
        if self.df is None:
            print("Error: No data loaded")
            return None, None
        df = self.df.copy()
        # Only use columns that actually exist in the dataframe
        available_feature_cols = [
            'QUANTITYORDERED', 'PRICEEACH', 'MSRP', 'QTR_ID', 'MONTH_ID', 'YEAR_ID',
            'DEALSIZE_NUMERIC', 'STATUS_NUMERIC', 'TERRITORY_RANK', 'ORDERLINENUMBER',
            'YEAR', 'MONTH', 'DAY', 'DAYOFWEEK', 'QUARTER', 'PROFIT_MARGIN',
            'TOTAL_QUANTITY', 'AVG_SALES', 'ORDER_COUNT'
        ]
        # Filter to only include columns that exist
        feature_cols = [col for col in available_feature_cols if col in df.columns]
        
        if not feature_cols:
            print("Warning: No valid feature columns found")
            return None, None
            
        X = df[feature_cols]
        y = df[target] if target in df.columns else None
        return X, y

    def get_feature_columns(self):
        return [
            'QUANTITYORDERED', 'PRICEEACH', 'MSRP', 'QTR_ID', 'MONTH_ID', 'YEAR_ID',
            'DEALSIZE_NUMERIC', 'STATUS_NUMERIC', 'TERRITORY_RANK', 'ORDERLINENUMBER',
            'YEAR', 'MONTH', 'DAY', 'DAYOFWEEK', 'QUARTER', 'PROFIT_MARGIN',
            'TOTAL_QUANTITY', 'AVG_SALES', 'ORDER_COUNT'
        ]
    
    def get_features_for_modeling(self, target='TOTAL_PROFIT'):
        """Get features and target for modeling - alias for prepare_model_data"""
        return self.prepare_model_data(target)