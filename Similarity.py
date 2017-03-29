from pprint import pprint
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from collections import defaultdict
from gensim import corpora, models
from gensim.similarities import Similarity
import os
from Reader import Reader


#texts are the two sentences you are comparing with
texts = ["Human machine interface for lab abc computer applications",
         "The man went on the interface and figured out how to run the program"]

#I want documents to be every sentence in the entire test/train set
documents = ["Human machine interface for lab abc computer applications",
             "System and human system engineering testing of EPS",
"A survey of user opinion of computer system response time",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey",
             "The intersection graph of paths in trees",
             "The generation of random binary unordered trees",
             "Relation of user perceived response time to error measurement"]


model = models.KeyedVectors.load_word2vec_format(r'C:\Users\CCrowe\Downloads\GoogleNews-vectors-negative300.bin.gz', binary=True)

class Similar():
    def __init__(self,documents,texts):
        self.CompareSentences(documents,texts)

    def DictAlreadyExists(self):
        if (os.path.exists("quora.dict")):
            return True
        else:
            return False

    def CorpusAlreadyExists(self):
        if (os.path.exists("quora.mm")):
            return True
        else:
            return False

    def SetUp(self,documents,texts):
        self.new_documents = texts + documents
        if not self.DictAlreadyExists() and not self.CorpusAlreadyExists():
            print("dict or corpora do not exist")
            self.vectorizedTexts = self.GetVectorizedText(documents)
        else:
            self.vectorizedTexts = []
        self.dictionary = self.GetDictionary(self.vectorizedTexts)
        self.corpus = self.GetCorpus(self.dictionary,self.vectorizedTexts)
        
    def CompareSentences(self,documents,texts):
        self.SetUp(documents,texts)
        self.tsim,self.lsim = self.GetSimilarities(self.dictionary,self.corpus)
        #self.PrintSimilar(self.tsim,self.lsim,self.new_documents)

    def PrintSimilar(self,tsim,lsim,documents):
        for tsim,lsim,sent in zip(tsim,lsim,documents):
            print(tsim,lsim,sent)

    def GetVectorizedText(self,documents):
        texts = self.VectorizeTextList(documents)
        return texts
    
    def GetDictionary(self,texts):
        if self.DictAlreadyExists():
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
        if self.CorpusAlreadyExists():
            corpus = corpora.MmCorpus('quora.mm')
        else:
            corpus = [dictionary.doc2bow(text) for text in texts]
            corpora.MmCorpus.serialize('quora.mm', corpus)
        return corpus

    def GetLsm(self,dictionary,corpus):
        lsi = models.lsimodel.LsiModel(corpus,id2word=dictionary)#num_topics=len(corpus)/2
        vec_lsi = lsi[corpus[0]]
        index = Similarity('l_index',corpus,len(dictionary))
        cnt = 0
        for similarities in index:
            if cnt == 1:
                return list(enumerate(similarities))
            cnt += 1
            
        #return list(enumerate(lsims))
    def GetWord2Vec(self,dictionary,corpus):
        model = models.Word2Vec(self.new_documents, size=100, window=5, min_count=5, workers=4)
        model.build_vocab(self.new_documents, update=True)
        model.train(self.new_documents)
        file_name = 'word2vec.model'
        model.save(file_name)
        model = models.Word2Vec.load(file_name)
        print(model.wv.similarity(self.new_documents[0].lower().split(),self.new_documents[1].lower().split()))

    def GetTfidf(self,dictionary,corpus):
        tfidf = models.TfidfModel(corpus)
        vec_lsi = tfidf[corpus[0]]
        index = Similarity('t_index',corpus,len(dictionary))
        #tsims = index[vec_lsi]
        cnt = 0
        for similarities in index:
            if cnt == 1:
                return list(enumerate(similarities))
            cnt += 1
        #return list(enumerate(tsims))
    
    def GetSimilarities(self,dictionary,corpus):
        self.GetWord2Vec(dictionary,corpus)
        #print("lsims")
        lsims = self.GetLsm(dictionary,corpus)
        #print("tsims")
        tsims = self.GetTfidf(dictionary,corpus)
        return (tsims,lsims,)


if __name__ == '__main__':
    reader = Reader(r"C:\Users\CCrowe\Documents\Kaggle\Quora\train.csv",r"C:\Users\CCrowe\Documents\Kaggle\Quora\test.csv")
    documents = reader.GetDocuments()
    print("documents retrieved")
    similar = Similar(documents,texts)









