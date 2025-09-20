import pandas as pd
import numpy as np

def parse_and_clean_file(file_path: str) -> pd.DataFrame:
    # Read file based on extension
    if file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Only CSV and XLSX are supported.")
    
    # Normalize column names: lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Define expected schema for reference
    expected_columns = {
        'studentid': 'Int64',  # nullable integer type in pandas
        'name': 'string',
        'attendance': 'float',
        'score': 'float',
        'feespayed': 'float',  # example column, adjust as needed
        'date_of_birth': 'datetime64[ns]'  # example date column
    }
    
    # Keep only expected columns and add missing columns with NaN
    for col in expected_columns:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[list(expected_columns.keys())]
    
    # Convert columns to expected types
    for col, dtype in expected_columns.items():
        if dtype == 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif dtype == 'string':
            df[col] = df[col].astype('string')
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)
    
    # Handle missing data:
    # Example rules:
    # - For numeric columns, fill missing with median
    # - For string columns, fill missing with 'Unknown'
    # - For datetime columns, fill missing with a default date or leave as NaT
    
    for col, dtype in expected_columns.items():
        if dtype in ['float', 'Int64']:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
        elif dtype == 'string':
            df[col] = df[col].fillna('Unknown')
        elif dtype == 'datetime64[ns]':
            # Example: fill missing DOB with 2000-01-01 or leave as is
            df[col] = df[col].fillna(pd.Timestamp('2000-01-01'))
    
    # Optionally, drop rows with corrupted critical data (e.g., missing mandatory IDs)
    df = df.dropna(subset=['studentid'])
    
    return df

# Example usage:
if __name__ == "__main__":
    cleaned_df = parse_and_clean_file('data/student_data.csv')
    print(cleaned_df.head())
