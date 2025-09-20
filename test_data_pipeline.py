import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from io import StringIO

# Sample functions simulating your pipeline components

def parse_file(file_like) -> pd.DataFrame:
    df = pd.read_csv(file_like)
    # normalization example: lowercase columns
    df.columns = df.columns.str.lower()
    # simple cleaning: drop rows with missing studentid
    df = df.dropna(subset=['studentid'])
    df['studentid'] = df['studentid'].astype(int)
    return df

def merge_datasets(dfs):
    # outer join on studentid
    merged = dfs[0]
    for df in dfs[1:]:
        merged = pd.merge(merged, df, on='studentid', how='outer')
    return merged.drop_duplicates(subset='studentid')

def store_dataframe(df, filename):
    df.to_csv(filename, index=False)

# Test class

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        # Sample CSV data as string
        self.attendance_csv = StringIO("""studentid,attendance\n1,90\n2,85\n3,78\n""")
        self.assessments_csv = StringIO("""studentid,score\n1,88\n2,92\n3,79\n""")
        self.fees_csv = StringIO("""studentid,fees_paid\n1,1000\n2,950\n3,1100\n""")
    
    def test_parse_file(self):
        df = parse_file(self.attendance_csv)
        expected = pd.DataFrame({
            'studentid': [1, 2, 3],
            'attendance': [90, 85, 78]
        })
        assert_frame_equal(df, expected)
    
    def test_merge_datasets(self):
        attendance = parse_file(self.attendance_csv)
        assessments = parse_file(self.assessments_csv)
        fees = parse_file(self.fees_csv)
        
        merged = merge_datasets([attendance, assessments, fees])
        
        expected = pd.DataFrame({
            'studentid': [1, 2, 3],
            'attendance': [90, 85, 78],
            'score': [88, 92, 79],
            'fees_paid': [1000, 950, 1100]
        })
        
        # Merge may rearrange columns, sort columns for comparison
        merged = merged[expected.columns]
        assert_frame_equal(merged, expected)
    
    def test_store_and_load(self):
        # Testing CSV storage and reload
        attendance = parse_file(self.attendance_csv)
        store_dataframe(attendance, 'test_output.csv')
        
        reloaded = pd.read_csv('test_output.csv')
        reloaded.columns = reloaded.columns.str.lower()  # normalize
        assert_frame_equal(attendance, reloaded)
    
    def test_performance_load(self):
        # Simple load test by merging dataframes multiple times (mock)
        attendance = parse_file(self.attendance_csv)
        assessments = parse_file(self.assessments_csv)
        fees = parse_file(self.fees_csv)
        
        dfs = [attendance, assessments, fees] * 100  # simulate load
        
        merged = merge_datasets(dfs)
        self.assertTrue(len(merged) == 3)  # Should still have 3 unique students
    
    # Document known issue example
    # def test_known_issue(self):
    #     # Known issue: missing studentid rows cause failure in parse_file
    #     pass

if __name__ == '__main__':
    unittest.main()
