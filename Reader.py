from pandas import read_csv

class Reader():
    def __init__(self,train_path,test_path):
        self.documents = []
        self.documents += self.GetTrainSentences(train_path)
        self.documents += self.GetTestSentences(test_path)
    def GetDocuments(self):
        return self.documents
    def GetTrainSentences(self,train_path):
        l = []
        cnt = 0
        df = read_csv(train_path)
        for row in df.itertuples():
            l.append(row[4])
            l.append(row[5])
            cnt += 1
            if cnt == 10000:
                break
        return l
    def GetTestSentences(self,test_path):
        l = []
        cnt = 0
        df = read_csv(test_path)
        for row in df.itertuples():
            l.append(row[2])
            l.append(row[3])
            cnt += 1
            if cnt == 10000:
                break
        return l
    

reader = Reader(r"C:\Users\CCrowe\Documents\Kaggle\Quora\train.csv",r"C:\Users\CCrowe\Documents\Kaggle\Quora\test.csv")
documents = reader.GetDocuments()
