import unittest
import os
import pandas as pd
from analysis import load_epr_data  # Import the loading function from your main script

class TestEPRDataIntegrity(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the list of expected filenames based on the experiment structure.
        Executed before each test method.
        """
        self.systems = ['LOV_EDTA_0_1M', 'LOV_EDTA_0_1M_FMN_200uM']
        self.conditions = ['dark', 'light']
        self.capillaries = ['01', '02', '03']
        
        self.expected_files = []
        for sys in self.systems:
            for cond in self.conditions:
                for cap in self.capillaries:
                    # Constructing the expected filename pattern
                    self.expected_files.append(f"{sys}_{cond}_{cap}(in).csv")

    def test_1_files_exist(self):
        """
        Task 1: Verify that all required files exist in the current working directory.
        """
        missing_files = []
        for filename in self.expected_files:
            if not os.path.exists(filename):
                missing_files.append(filename)
        
        # Check if the list of missing files is empty
        self.assertEqual(len(missing_files), 0, f"The following files are missing: {missing_files}")

    def test_2_and_3_load_and_content(self):
        """
        Task 2 & 3: Verify that files can be parsed correctly and contain valid EPR data.
        """
        for filename in self.expected_files:
            # Skip check if file doesn't exist to avoid redundant errors (handled in test 1)
            if os.path.exists(filename):
                df = load_epr_data(filename)
                
                # Task 2: Ensure the data loader returns a valid DataFrame and not None
                self.assertIsNotNone(df, f"Failed to read file: {filename}")
                
                # Task 3: Check if the DataFrame is not empty
                self.assertFalse(df.empty, f"File is empty: {filename}")
                
                # Task 3: Verify that 'Field' and 'Intensity' columns are present
                self.assertIn('Field', df.columns, f"Missing 'Field' column in: {filename}")
                self.assertIn('Intensity', df.columns, f"Missing 'Intensity' column in: {filename}")
                
                # Task 3: Verify data quantity (ensure there are enough data points for a spectrum)
                self.assertGreater(len(df), 10, f"Insufficient data points in: {filename}")

if __name__ == '__main__':
    # Run all tests defined in the class
    unittest.main()