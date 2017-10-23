import numpy as np
from sklearn.svm import SVC

X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
y = np.array([1, 1, 2, 2])

clf = SVC()
clf.fit(X, y) 
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
predict_Y=clf.predict(test_X)

precision=0.0

for i in range(len(predict_Y)):
	if predict_Y[i]==test_Y[i]:
		precision+=1

print "precision is: ",precision/len(predict_Y)		
