import unittest
import csv
import os
from Globals import main_dir

class TestRows(unittest.TestCase):
    def CountRows(self,path):
        count = 0
        with open(path, 'r') as count_file:
            csv_reader = csv.reader(count_file)
            for row in csv_reader:
                count += 1
        print("Should be:" + str(2345797))
        self.assertEqual(count,2345797)

def RunTests():
    test = TestRows()
    test.CountRows(os.path.join(main_dir,"sample_submission.csv"))

if __name__ == '__main__':
    test = TestRows()
    test.CountRows(os.path.join(main_dir,"sample_submission.csv"))
