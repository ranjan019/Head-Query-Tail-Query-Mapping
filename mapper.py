import sys
import gensim
import keras
import numpy as np
from keras.models import load_model

HEAD_QUERY_PATH = './head150.txt'
Word2vec_PATH = './w2vNet.model'
word2vecLen = 100

def wordTovec2(headQuery,model):
	head_embedding=np.ndarray(shape=(word2vecLen/2,), dtype=float, order='F')
	head_query=headQuery.replace('.',' ').split(" ")
	for word in head_query:
		if word in model.wv.vocab:
			head_embedding+=model[word]
	head_embedding/=len(head_query)
	return head_embedding

def createHeadVectors(model):
    head_queries = []
    with open(HEAD_QUERY_PATH) as f:
        for line in f:
            head_queries.append(line.strip())
    l1 = len(head_queries)
    head_X = np.zeros((l1,word2vecLen/2),dtype=float)
    for i in range(l1):
        head_X[i] = wordTovec2(head_queries[i],model)

    return np.asarray(head_queries),head_X

# if __name__== "__main__":
#     model = gensim.models.Word2Vec.load(Word2vec_PATH)
#     tail_query = sys.argv[1]
#     tail_vector = wordTovec2(tail_query,model)
#     neuralNetModel = load_model('my_model.h5')
#     head_queries , head_X = createHeadVectors(model)
#     l1 = len(head_X)
#     for i in range(l1):
#         test = [np.append(head_X[i],tail_vector)]
#         print head_queries[i],neuralNetModel.predict(test)
