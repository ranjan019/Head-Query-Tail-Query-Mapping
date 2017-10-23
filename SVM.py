import numpy as np
from sklearn.svm import SVC
import pydexter
from sentence_similarity import calcQuerySimilarity
from gensim.models import word2vec
from cosine_similarity import calcCosineSimilarity
from entity_check import calcEntityCheck


def calcJaccard(list1,list2):
    s1=set(list1)
    s2=set(list2)
    inters=s1.intersection(s2)
    uni=s1.union(s2)
    return float(len(inters))/len(uni)

def makingQueryPairVector(query1, query2,model,dxtr):
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
    sentences=word2vec.Text8Corpus('/home/pulkit/IIIT-H/NLP_Project/text8')
    model=word2vec.Word2Vec(sentences,size=10)

    # creating the dexter client
	dxtr = pydexter.DexterClient("http://dexterdemo.isti.cnr.it:8080/dexter-webapp/api/")

	# processing the query log to obtain training and test data
	train_feature_matrix=[]
	train_labels=[]

	with open("train_data.txt","r") as train_data:
		for sample in train_data:
			items=sample.split("~")
			train_feature_vector=makingQueryPairVector(items[0],items[1],model,dxtr)
			train_labels.append(items[2])
			train_feature_matrix.append(train_feature_vector)

	test_feature_matrix=[]
	test_labels=[]

	with open("test_data.txt","r") as test_data:
		for sample in test_data:
			items=sample.split("~")
			test_feature_vector=makingQueryPairVector(items[0],items[1],model,dxtr)
			test_labels.append(items[2])
			test_feature_matrix.append(test_feature_vector)


	
	train_X=np.array(train_feature_matrix)
	train_Y = np.array(train_labels)

	test_X=np.array(test_feature_matrix)
	test_Y=np.array(test_labels)

	#preapring the model adn training it
	SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
	    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
	    max_iter=-1, probability=False, random_state=None, shrinking=True,
	    tol=0.001, verbose=False)

	
	clf = SVC()
	clf.fit(train_X,train_Y)

	#testing the model
	predict_Y=clf.predict(test_X)

	precision=0.0

	for i in range(len(predict_Y)):
		if predict_Y[i]==test_Y[i]:
			precision+=1

	print "precision is: ",precision/len(predict_Y)
