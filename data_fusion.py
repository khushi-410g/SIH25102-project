import pandas as pd
from functools import reduce

def resolve_duplicates(df: pd.DataFrame, id_col: str) -> pd.DataFrame:
    """
    Resolves duplicate student records by keeping the first one and logging others.
    This can be enhanced with complex conflict resolution logic.
    """
    duplicates = df[df.duplicated(subset=[id_col], keep=False)]
    if len(duplicates) > 0:
        print(f"Warning: {len(duplicates)} duplicate student records found. Keeping first occurrence.")
    # For simplicity, keep first occurrence
    df = df.drop_duplicates(subset=[id_col], keep='first')
    return df

def merge_datasets(dfs: list, on: str = 'studentid', how: str = 'outer') -> pd.DataFrame:
    """
    Merges multiple dataframes on the given key column using outer join to preserve all data.
    """
    merged_df = reduce(lambda left, right: pd.merge(left, right, on=on, how=how), dfs)
    merged_df = resolve_duplicates(merged_df, id_col=on)
    return merged_df

def add_versioning(df: pd.DataFrame, version_col: str = 'version', version: int = 1) -> pd.DataFrame:
    """
    Adds a version column to the dataframe for simple versioning.
    """
    df[version_col] = version
    return df

def store_to_csv(df: pd.DataFrame, file_name: str):
    """
    Stores the dataframe to a CSV file.
    """
    df.to_csv(file_name, index=False)
    print(f"Data successfully stored to {file_name}")

# Example usage:
if __name__ == "__main__":
    # Loading example datasets (replace with your actual file paths or data sources)
    attendance = pd.DataFrame({
        'studentid': [1, 2, 3],
        'attendance': [90, 85, 78]
    })

    assessments = pd.DataFrame({
        'studentid': [1, 2, 3],
        'score': [88, 92, 79]
    })

    fees = pd.DataFrame({
        'studentid': [1, 2, 3],
        'fees_paid': [1000, 950, 1100]
    })

    # Merge datasets on 'studentid'
    merged = merge_datasets([attendance, assessments, fees], on='studentid', how='outer')

    # Add versioning
    merged = add_versioning(merged, version=1)

    # Print resulting dataframe
    print("Consolidated Student Profiles:")
    print(merged)

    # Store to CSV
    store_to_csv(merged, 'merged_student_profiles_v1.csv')
