import sys
import numpy as np
import keras
import numpy as np
# import pydexter
from keras import optimizers
import pdb
from gensim.models import Word2Vec
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from gensim.models.keyedvectors import KeyedVectors

word2vecLen = 600 #300 for each query

def wordTovec(headQuery,tailQuery,model):
	# print headQuery
	head_embedding=np.ndarray(shape=(word2vecLen/2,), dtype=float, order='F')
	head_query=headQuery.replace('.',' ').split(" ")
	for word in head_query:
		if word in model.wv.vocab:
			# pdb.set_trace()
			head_embedding+=model[word]
	head_embedding/=len(head_query)
	tail_embedding=np.ndarray(shape=(word2vecLen/2,), dtype=float, order='F')
	# pdb.set_trace()
	tail_query=tailQuery.replace('.',' ').split(" ")
	for word in tail_query:
		if word in model.wv.vocab:
			tail_embedding+=model[word]
	tail_embedding/=len(tail_query)
	pair_embedding = np.append(head_embedding,tail_embedding)
	return pair_embedding

def NeuralNet(train_X,train_Y):
	model = Sequential()
	model.add(Dense(word2vecLen,activation='tanh',input_dim=word2vecLen))
	model.add(Dense(10,activation='tanh'))
	model.add(Dropout(0.23))
	model.add(Dense(10,activation='tanh'))
	model.add(Dropout(0.26))
	model.add(Dense(1,activation='sigmoid'))
	# model.add(Dropout(0.29))
	sgd = optimizers.SGD(lr=0.01, clipnorm=1.)
	model.compile(optimizer=sgd,
              loss='binary_crossentropy',
              metrics=['accuracy'])

	model.fit(train_X,train_Y,
					batch_size = 50,
					epochs = 80,
					validation_split=0.2,
					shuffle=True,
					verbose=1)
	return model

def findAnswers(x_test,model):
	final_ans = model.predict(x_test)
	for i in range(len(final_ans)):
		if final_ans[i]>=0.5:
			final_ans[i] = 1
		else:
			final_ans[i] = 0
	return final_ans

def findAccuracy(y_test,actual_ans):
	co = 0
	for i in range(len(y_test)):
		if(y_test[i]==actual_ans[i]):
			co+=1;
	return co/len(y_test)

if __name__== "__main__":
	data = []
	Word2vec_PATH = './word2vec__GoogleNews_100Bwords__300Dvectors__3M_vocab.bin'
	with open(sys.argv[1],'r') as f:
		for l in f:
			data.append(l)
	# print len(data)
	modelVec = KeyedVectors.load_word2vec_format(Word2vec_PATH, binary=True)
	total_data = len(data)
	train_data_word = data[:int(0.8*total_data)]
	l1 = len(train_data_word)
	test_data_word = data[int(0.8*total_data):]
	l2 = len(test_data_word)
	train_X = np.zeros((l1,word2vecLen),dtype=float)
	train_Y = np.zeros((l1,1),dtype=int)
	test_X = np.zeros((l2,word2vecLen),dtype=float)
	test_Y = np.zeros((l2,1),dtype=int)
	i = 0
	for pair in train_data_word:
		head_tail = pair.split(',')
		# pdb.set_trace()
		train_X[i] = wordTovec(head_tail[0].strip(),head_tail[1].strip(),modelVec)
		train_Y[i] = int(head_tail[2].strip())
		if(train_Y[i]==-1):
			train_Y[i] = 0
		i += 1

	i = 0
	for pair in test_data_word:
		head_tail = pair.split(',')
		test_X[i] = wordTovec(head_tail[0].strip(),head_tail[1].strip(),modelVec)
		test_Y[i] = int(head_tail[2].strip())
		if(test_Y[i]==-1):
			test_Y[i] = 0
		i += 1

	# for i in range(l1):
	# 	print train_X[i]
	modelNet = NeuralNet(train_X,train_Y)
	finalAns = findAnswers(test_X,modelNet)
	print finalAns
