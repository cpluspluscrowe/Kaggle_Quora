from pprint import pprint
from collections import defaultdict
from gensim import corpora, models, similarities

#texts are the two sentences you are comparing with
texts = ["Human machine interface for lab abc computer applications",
         "System and human system engineering testing of EPS"]

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
    def GetDictionary(self,documents):
        dictionary = self.BagOfWords(documents)
        return dictionary

    def VectorizeTextList(self,textList):
        stoplist = set('for a of the and to in'.split())
        texts = [[word for word in document.lower().split() if word not in stoplist] for document in textList]

        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1] for text in texts]
        return texts
    def GetCorpus(self,textList):
        texts = self.VectorizeTextList(textList)
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        return corpus
        
    def CompareSentences(self,documents,texts):
        new_documents = documents + texts
        self.dictionary = self.GetDictionary(new_documents)
        self.corpus = self.GetCorpus(new_documents)#texts
        how_similar = self.GetSimilarities(self.dictionary,self.corpus)
        print(how_similar)

    def BagOfWords(self,documents):
        texts = self.VectorizeTextList(documents)
        dictionary = corpora.Dictionary(texts)
        return dictionary


    def GetSimilarities(self,dictionary,corpus):
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
        #doc = "Human computer interaction"
        #vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[corpus[0]]
        index = similarities.MatrixSimilarity(lsi[corpus])
        sims = index[vec_lsi]
        return list(enumerate(sims))[1][1]

similar = Similar(documents,texts)










