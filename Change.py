from Algorithm import Algorithm
from Submit import CreateSubmissionCSV
import sqlite3 as lite
import os
from Globals import main_dir

class Changer():
    def __init__(self):
        self.algorithm = Algorithm()
        self.conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        self.cur = self.conn.cursor()
        self.cur.execute('''select id,question1,question2 from test''')
        rows = self.cur.fetchall()
        for row in rows:
            answer = self.algorithm.apply(row[1],row[2])
            self.ApplyChangeInDatabase(row[0],answer)
        self.conn.commit()
        self.conn.close()
    def ApplyChangeInDatabase(self,id,result):
        self.cur.execute('''update test set is_duplicate = ? where id = ?''',(result,id,))

if __name__ == '__main__':
    changer = Changer()
    CreateSubmissionCSV()
