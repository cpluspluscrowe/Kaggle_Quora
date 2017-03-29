from pprint import pprint
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from collections import defaultdict
from gensim import corpora, models, similarities
import os
from Reader import Reader


#texts are the two sentences you are comparing with
texts = ["Human machine interface for lab abc computer applications",
         "Very Short Sentence"]

#I want documents to be every sentence in the entire test/train set
documents = ["Human machine interface for lab abc computer applications",
             "System and human system engineering testing of EPS",
"A survey of user opinion of computer system response time",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey",
             "The intersection graph of paths in trees",
             "The generation of random binary unordered trees",
             "Relation of user perceived response time to error measurement"]

class Similar():
    def __init__(self,documents,texts):
        self.CompareSentences(documents,texts)

    def SetUp(self,documents,texts):
        self.new_documents = texts + documents
        self.vectorizedTexts = self.GetVectorizedText(documents)
        self.dictionary = self.GetDictionary(self.vectorizedTexts)
        self.corpus = self.GetCorpus(self.dictionary,self.vectorizedTexts)
        
    def CompareSentences(self,documents,texts):
        self.SetUp(documents,texts)
        self.tsim,self.lsim = self.GetSimilarities(self.dictionary,self.corpus)
        #self.PrintSimilar(self.how_similar,self.how_similar2,self.new_documents)

    def PrintSimilar(self,tsim,lsim,documents):
        for tsim,lsim,sent in zip(how_similar,how_similar2,documents):
            print(tsim,lsim,sent)

    def GetVectorizedText(self,documents):
        texts = self.VectorizeTextList(documents)
        return texts
    
    def GetDictionary(self,texts):
        if (os.path.exists("quora.dict")):
            dictionary = corpora.Dictionary.load('quora.dict')
        else:
            dictionary = corpora.Dictionary(texts)
            dictionary.save('quora.dict')
        return dictionary

    def FormatText(self,textList):
        docList = []
        for document in textList:
            l = []
            if type(document) is str:
                spl = document.split()
                for word in spl:
                    if not word.isdigit():
                        l.append(word.lower())
            else:
                pass#nan documents
            docList.append(l)
        return docList
            
    def VectorizeTextList(self,textList):
        stoplist = set('for a of the and to in'.split())
        texts = self.FormatText(textList)  #[[word for word in document.lower().split() if word not in stoplist] for document in textList]

        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1] for text in texts]
        return texts
    def GetCorpus(self,dictionary,texts):
        if (os.path.exists("quora.mm")):
            corpus = corpora.MmCorpus('quora.mm')
        else:
            corpus = [dictionary.doc2bow(text) for text in texts]
            corpora.MmCorpus.serialize('quora.mm', corpus)
        return corpus

    def GetLsm(self,dictionary,corpus):
        lsi = models.lsimodel.LsiModel(corpus,id2word=dictionary, num_topics=len(corpus)/2)
        vec_lsi = lsi[corpus[0]]
        index = similarities.MatrixSimilarity(lsi[corpus])
        lsims = index[vec_lsi]
        return list(enumerate(lsims))

    def GetTfidf(self,dictionary,corpus):
        tfidf = models.TfidfModel(corpus)#, id2word=dictionary, num_topics=len(corpus)/2
        vec_lsi = tfidf[corpus[0]]
        index = similarities.MatrixSimilarity(tfidf[corpus],len(dictionary))
        tsims = index[vec_lsi]
        return list(enumerate(tsims))
    
    def GetSimilarities(self,dictionary,corpus):
        tsims = self.GetLsm(dictionary,corpus)
        lsims = self.GetTfidf(dictionary,corpus)
        return (tsims[1][1],lsims[1][1][1],)


if __name__ == '__main__':
    reader = Reader(r"C:\Users\CCrowe\Documents\Kaggle\Quora\train.csv",r"C:\Users\CCrowe\Documents\Kaggle\Quora\test.csv")
    documents = reader.GetDocuments()
    similar = Similar(documents,texts)
    print(similar.tsim,similar.lsim)









