import pandas as pd

# File paths (update these paths to your actual spreadsheet locations)
attendance_file = 'attendance.xlsx'
test_scores_file = 'test_scores.xlsx'
fee_payment_file = 'fee_payment.xlsx'

# Load spreadsheets into DataFrames
attendance_df = pd.read_excel(attendance_file)
test_scores_df = pd.read_excel(test_scores_file)
fee_payment_df = pd.read_excel(fee_payment_file)

# Preview loaded data (optional)
print("Attendance Data Sample:")
print(attendance_df.head())
print("\nTest Scores Data Sample:")
print(test_scores_df.head())
print("\nFee Payment Data Sample:")
print(fee_payment_df.head())

# Data Cleaning & Preprocessing

# Standardize column names (lowercase, strip spaces)
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

attendance_df = clean_columns(attendance_df)
test_scores_df = clean_columns(test_scores_df)
fee_payment_df = clean_columns(fee_payment_df)

# Handle missing values - example: fill missing attendance with 0, test scores with mean, fee status with 'Unpaid'
attendance_df['attendance_percentage'] = attendance_df['attendance_percentage'].fillna(0)
test_scores_df['test_score'] = test_scores_df['test_score'].fillna(test_scores_df['test_score'].mean())
fee_payment_df['fee_status'] = fee_payment_df['fee_status'].fillna('Unpaid')

# Ensure common student identifier column exists and is consistent
# Assuming 'student_id' is the common key in all files
for df in [attendance_df, test_scores_df, fee_payment_df]:
    if 'student_id' not in df.columns:
        raise ValueError("Missing 'student_id' column in one of the datasets")

# Merge datasets on 'student_id'
merged_df = attendance_df.merge(test_scores_df, on='student_id', how='outer') \
                         .merge(fee_payment_df, on='student_id', how='outer')

# Optional: Fill any remaining missing values after merge
merged_df.fillna({'attendance_percentage': 0, 'test_score': 0, 'fee_status': 'Unpaid'}, inplace=True)

# Save merged data to a new Excel file
merged_df.to_excel('merged_student_data.xlsx', index=False)

print("\nMerged Data Sample:")
print(merged_df.head())
print("\nMerged data saved to 'merged_student_data.xlsx'")
