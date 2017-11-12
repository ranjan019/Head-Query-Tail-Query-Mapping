import numpy as np
from sklearn.svm import SVC
import pydexter
from sentence_similarity import calcQuerySimilarity
# import sentence_similarity
from gensim.models import Word2Vec
from cosine_similarity import calcCosineSimilarity
from entity_check import calcEntityCheck


def calcJaccard(list1,list2):
	s1=set(list1)
	s2=set(list2)
	inters=s1.intersection(s2)
	uni=s1.union(s2)
	if len(uni)==0:
		return 0

	return float(len(inters))/len(uni)

def makingQueryPairVector(query1, query2,model,dxtr):

	#print "making feature vector"
	list1=query1.split()
	list2=query2.split()
	jcoef=calcJaccard(list1,list2)
	querypairvector=[]
	querypairvector.append(jcoef)
	sentsim=calcQuerySimilarity(query1,query2)
	querypairvector.append(sentsim)
	cossim = calcCosineSimilarity(query1,query2,model)
	querypairvector.append(cossim)
	namedentitysc=calcEntityCheck(query1,query2,dxtr) #3rd argument dxtr?????????
	querypairvector.append(namedentitysc)
	return querypairvector


if __name__ == '__main__':


	#configuring the word2vec
	print "training word2vec"
	#sentences=word2vec.Text8Corpus('text8')
	#model=word2vec.Word2Vec(sentences,size=10)
	#model = Word2Vec.load('cosModel.model')

	# creating the dexter client
	print "creating dexter client"
	dxtr = pydexter.DexterClient("http://dexterdemo.isti.cnr.it:8080/dexter-webapp/api/")

	# processing the query log to obtain training and test data
	train_feature_matrix=np.array([])
	train_labels=np.array([])
	"""i = 0
	f1 = open('trainFeatureVector.txt','w')
	with open("train2.txt","r") as train_data:
		for sample in train_data:
			#print "reading training sample", ':' ,i
			items=sample.split(",")
			train_feature_vector=makingQueryPairVector(items[0],items[1],model,dxtr)
			f1.write(' '.join(str(x) for x in train_feature_vector) + ' ' + str(items[2]))
			#train_labels.append(items[2])
			#train_feature_matrix.append(train_feature_vector)
			i += 1
	f1.close()
	"""
	test_feature_matrix=np.array([])
	test_label=np.array([])
	i = 0
	#f1 = open('testFeatureVector.txt','w')
	with open("DATA/finalFeature.txt","r") as test_data:
		for sample in test_data:
			#print "reading test sample",':',i
			items=sample.split(" ")
			#print items
			test_feature_vector=np.asfarray(items[:-2])
			t = np.asfarray(items[-1])
			if test_label.size:
				test_label = np.append(test_label,t)
				test_feature_matrix = np.concatenate((test_feature_matrix,[test_feature_vector]),axis=0)
			else :
				test_label = t
				test_feature_matrix = [test_feature_vector]


	#print np.shape(test_feature_matrix),np.shape(test_label)

	train_X=np.array(test_feature_matrix[:-6000])
	train_Y = np.array(test_label[:-6000])

	test_X=np.array(test_feature_matrix[-6000:])
	test_Y=np.array(test_label[-6000:])
	co = 0
	for i in range(len(test_Y)):
		if test_Y[i] == 1:
			co += 1

	#preapring the model adn training it
	print "Model set up "
	SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
		decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
		max_iter=-1, probability=False, random_state=None, shrinking=True,
		tol=0.001, verbose=False)

	clf = SVC()
	clf.fit(train_X,train_Y)

	#testing the model
	predict_Y=clf.predict(test_X)

	precision=0.0
	coP = 0
	coN = 0
	for i in range(len(predict_Y)):
		if predict_Y[i]==1:
			coP += 1
		else:
			coN += 1
		if predict_Y[i]==test_Y[i]:
			precision+=1

	print "precision is: ",precision/len(predict_Y)
	print co,coP,coN
