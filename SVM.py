import numpy as np
from sklearn.svm import SVC
import pydexter
from sentencesimilarity


def makingQueryPairVector(query1, query2):
	list1=query1.split()
	list2=query2.split()
	jcoef=calcJaccard(list1,list2)
	querypairvector=[]
	querypairvector.append(jcoef)
	sentsim=calcQuerySimilarity(query1,query2)
	querypairvector.append(sentsim)
 


X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
y = np.array([1, 1, 2, 2])

clf = SVC()
clf.fit(X, y) 
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
print(clf.predict([[-0.8, -1]]))
