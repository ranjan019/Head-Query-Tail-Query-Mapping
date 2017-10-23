import numpy as np

def calcCosineSimilarity(headQuery,tailQuery,model):
	# calculating the head query features

	#head query embedding
	head_embedding=np.ndarray(shape=(10,), dtype=float, order='F')

	head_query=headQuery.replace('.',' ').split(" ")
    
    	for word in head_query:
        	if word in model.wv.vocab:
            		head_embedding+=model[word]
    
    	head_embedding/=len(head_query)
    
    	#check if head_embedding is 0
    	#print head_query,": ",head_embedding


	# calculating the tail query features

	#tail query embeding
	tail_embedding=np.ndarray(shape=(10,), dtype=float, order='F')

    	tail_query=tailQuery.replace('.',' ').split(" ")
    
    	for word in tail_query:
        	if word in model.wv.vocab:
            		tail_embedding+=model[word]
        
    	tail_embedding/=len(tail_query) 
    
    	#check if tail_embedding is 0
   	# print tail_query,": ",tail_embedding    


	# calculating the cosine similarity
	cosine_score=np.dot(head_embedding,tail_embedding)

	return cosine_score
    
