from pandas import read_csv
import os

class Reader():
    def __init__(self,train_path,test_path):
        file_name = "Sentences.txt"
        if os.path.exists(file_name):
            self.documents = self.GetListFromFile(file_name)
        else:
            self.documents = []
            self.documents += self.GetTrainSentences(train_path)
            self.documents += self.GetTestSentences(test_path)
            self.documents = list(set(self.documents)) #get rid of duplicates
            self.WriteSentences(file_name)
    def GetListFromFile(self,file_name):
        documents = []
        with open(file_name, 'r', encoding="utf-8") as file:
            for line in file.readlines():
                documents.append(line)
        return documents
    def WriteSentences(self,file_name):
        with open(file_name, 'w', encoding="utf-8") as file:
            for doc in self.documents:
                if type(doc) is str:
                    file.write(doc + "\n")
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
            if cnt == 100:
                break#Change me to pass
        return l
    def GetTestSentences(self,test_path):
        l = []
        cnt = 0
        df = read_csv(test_path)
        for row in df.itertuples():
            l.append(row[2])
            l.append(row[3])
            cnt += 1
            if cnt == 100:
                break#Change me to pass
        return l
    

reader = Reader(r"C:\Users\CCrowe\Documents\Kaggle\Quora\train.csv",r"C:\Users\CCrowe\Documents\Kaggle\Quora\test.csv")
documents = reader.GetDocuments()
