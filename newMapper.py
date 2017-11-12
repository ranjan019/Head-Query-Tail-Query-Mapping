import numpy
import sys
import os
import pdb
from keras.models import load_model
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from lstm_rnn import createEmbeddingMatrix

def createCompatibleData(file_path,tokenizer,vecLength):
    tail = []
    with open(file_path,'r') as f:
        for l in f:
            tail.append(l.strip())

    sequences_tail = tokenizer.texts_to_sequences(tail)
    tail_data = pad_sequences(sequences_tail,maxlen=vecLength)

    return tail,np.asarray(tail_data)

if __name__== "__main__":
    file_path = sys.argv[1]
    tokenizer,embedding_matrix,head_data,tail_data,,word_index = createEmbeddingMatrix(file_path)
    file_path = './head150.txt'
    head_query,head_data = createCompatibleData(file_path,tokenizer,5)
    file_path = sys.argv[2]
    tail_query,tail_data = createCompatibleData(file_path,tokenizer,10)
    model = load_model('my_model1.h5')
    for query,i in tail_query:
        print "======================"
        for q,j in head_query:
            print tail_query," : ",q," : ",model.predict([head_data[j],tail_data[i]])
