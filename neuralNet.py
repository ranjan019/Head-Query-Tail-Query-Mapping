import sys
import keras
import numpy as np
# import pydexter
from keras import optimizers
import pdb
import gensim
from gensim.models import Word2Vec
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from gensim.models.keyedvectors import KeyedVectors
from mapper import *

word2vecLen = 100 #50 for each query

def wordTovec(headQuery,tailQuery,model):
	# print headQuery
	head_embedding=np.ndarray(shape=(word2vecLen/2,), dtype=float, order='F')
	head_query=headQuery.replace('.',' ').split(" ")
	#print head_query
	for word in head_query:
		#print word
		if word in model.wv.vocab:
			#pdb.set_trace()
			head_embedding+=model[word]
	head_embedding/=len(head_query)
	tail_embedding=np.ndarray(shape=(word2vecLen/2,), dtype=float, order='F')
	# pdb.set_trace()
	tail_query=tailQuery.replace('.',' ').split(" ")
	#print tail_query
	for word in tail_query:
		#print word
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
	sgd = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, clipnorm=1.)
	model.compile(optimizer=sgd,
              loss='binary_crossentropy',
              metrics=['accuracy'])

	model.fit(train_X,train_Y,
					batch_size = 5000,
					epochs = 80,
					validation_split=0.2,
					shuffle=True,
					verbose=1)
	return model

def findAnswers(x_test,model,train_Y):
	final_ans = model.predict(x_test)
	for i in range(len(final_ans)):
		print final_ans[i],
		if final_ans[i]>=0.5:
			final_ans[i] = 1
		else:
			final_ans[i] = 0
		print final_ans[i],train_Y[i]
	return final_ans

def findAccuracy(y_test,actual_ans):
	co = 0
	for i in range(len(y_test)):
		if(y_test[i]==actual_ans[i]):
			co+=1;
	return float((1.0*co)/len(y_test))

if __name__== "__main__":
	data = []
	#Word2vec_PATH = '../word2vec__GoogleNews_100Bwords__300Dvectors__3M_vocab.bin'
	Word2vec_PATH = './w2vNet.model'
	with open(sys.argv[1],'r') as f:
		for l in f:
			data.append(l)
	tailQueryList = []
	with open('./tailQuery.txt') as f:
		for l in f:
			tailQueryList.append(l)
	# print len(data)
	print "Loading Model Done"
	modelVec = gensim.models.Word2Vec.load(Word2vec_PATH)
	#modelVec = KeyedVectors.load_word2vec_format(Word2vec_PATH, binary=True)
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
	print "word2vec start"
	for pair in train_data_word:
		head_tail = pair.split('||')
		#pdb.set_trace()
		train_X[i] = wordTovec(head_tail[0].strip(),head_tail[1].strip(),modelVec)
		train_Y[i] = int(head_tail[2].strip())
		if(train_Y[i]==-1):
			train_Y[i] = 0
		i += 1
	print "phase2 of w2v"
	i = 0
	for pair in test_data_word:
		head_tail = pair.split('||')
		test_X[i] = wordTovec(head_tail[0].strip(),head_tail[1].strip(),modelVec)
		test_Y[i] = int(head_tail[2].strip())
		if(test_Y[i]==-1):
			test_Y[i] = 0
		i += 1

	modelNet = NeuralNet(train_X,train_Y)
	modelNet.save('my_model1.h5')
	finalAns = findAnswers(test_X,modelNet,train_Y)
	head_queries , head_X = createHeadVectors(modelVec)
	head_queries = head_queries.reshape(head_queries.shape[0],-1)
	for query in tailQueryList:
		print "================"
		print "Calculating for :", query
		tailVec =  wordTovec2(query,modelVec)
		l1 = len(head_queries)
		query_X = np.zeros((l1,word2vecLen),dtype=float)
		for i in range(len(head_queries)):
			query_X[i] = np.append(head_X[i],tailVec)
		queryAns = modelNet.predict(query_X)
		query_scorePair = np.concatenate((head_queries,queryAns),axis=1)
		# pdb.set_trace()
		query_scorePair = query_scorePair[np.argsort(query_scorePair[:, 1])]
		for i in range(5):
			print query," : ",query_scorePair[l1-i-1]

	#print findAccuracy(finalAns,train_Y)
	#f = open('output.txt','w')
	#for i in range(len(finalAns)):
		#f.write(finalAns[i])
		#print(finalAns[i],

	#f.close()
