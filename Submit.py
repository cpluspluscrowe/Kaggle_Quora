import csv
import sqlite3 as lite
import os
from Globals import main_dir
from Tests import RunTests

def CreateSubmissionCSV():
    csvWriter = csv.writer(open("sample_submission.csv", "w",newline=''))
    csvWriter.writerow(("test_id","is_duplicate",))
    conn = lite.connect(os.path.join(main_dir,'Quora.db'))
    cur = conn.cursor()
    cur.execute('''select id,is_duplicate from test''')
    rows = cur.fetchall()
    for row in rows:
        csvWriter.writerow(row)
    conn.commit()
    conn.close()
    RunTests()

if __name__ == '__main__':
    CreateSubmissionCSV()
