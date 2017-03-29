import os
from pandas import read_csv
import sqlite3 as lite
import xlwings as xw
from tqdm import tqdm
import csv
from Tests import TestRows
#r"C:\Users\CCrowe\Documents\Kaggle\Quora" #Everything is relative
from Globals import main_dir

def DeleteDatabase():
    os.remove("Quora.db")

class Train():
    def __init__(self):
        self.train_path_csv = os.path.join(main_dir,"train.csv")
        self.train_df = read_csv(self.train_path_csv)
        self.CreateTrainDatabase()
        self.LoadTrainData()
    def LoadTrainData(self):
        conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        cur = conn.cursor()
        for row in self.train_df.itertuples():
            cur.execute('''insert into train(id, qid1, qid2, question1, question2,is_duplicate) values(?,?,?,?,?,?)''',(row[1],row[2],row[3],row[4],row[5],0))
        conn.commit()
        conn.close()
    def PrintFromTrainDatabase(self,id,qid1,qid2,question1,question2):
        conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        cur = conn.cursor()
        cur.execute('''select id, qid1, qid2, question1, question2,is_duplicate from train where id = ? and qid1 = ?
                       and qid2 = ? and question1 = ? and question2 = ? and is_duplicate = ?''',(id,qid1,qid2,question1,question2,0))
        result = cur.fetchall()
        conn.commit()
        conn.close()
        #self.PrintFromTrainDatabase(id,qid1,qid2,question1,question2)
    def CreateTrainDatabase(self):
        conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS train(id integer, qid1 integer, qid2 integer, question1 text, question2 text,is_duplicate integer)''')
        conn.commit()
        conn.close()


class Test():
    def __init__(self):
        self.test_path_csv = os.path.join(main_dir,"test.csv")
        self.test_df = read_csv(self.test_path_csv)
        self.CreateTestDatabase()
        self.LoadTestData()
    def LoadTestData(self):
        conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        cur = conn.cursor()
        for row in self.test_df.itertuples():
            cur.execute('''insert into test(id,question1, question2, is_duplicate) values(?,?,?,?)''',(int(row[1]),row[2],row[3],0))
        conn.commit()
        conn.close()
    def PrintFromTestDatabase(self,id,qid1,qid2,question1,question2):
        conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        cur = conn.cursor()
        cur.execute('''select id, question1, question2,is_duplicate from test where id = ?
                       and question1 = ? and question2 = ? and is_duplicate = ?''',(id,question1,question2,0))
        result = cur.fetchall()
        print(result)
        conn.commit()
        conn.close()
        #self.PrintFromTrainDatabase(id,qid1,qid2,question1,question2)
    def CreateTestDatabase(self):
        conn = lite.connect(os.path.join(main_dir,'Quora.db'))
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS test(id integer, question1 text, question2 text,is_duplicate integer)''')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    DeleteDatabase()
    train = Train()
    test = Test()
    print("Done")

