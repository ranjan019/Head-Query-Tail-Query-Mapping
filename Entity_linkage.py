import numpy as np
import pydexter

def Entity_linkage(headQuery,tailQuery):

	dxtr=pydexter.DexterClient("http://dexterdemo.isti.cnr.it:8080/dexter-webapp/api/")
	head_result=dxtr.nice_annotate(headQuery, min_conf=0.8)
	# print head_entities
	head_entities=set()
	for item in head_result:
		if type(item)==tuple:
			head_entities.add(item[1])

	# print head_entities		

	# getting entites in the tail query
	tail_result=dxtr.nice_annotate(tailQuery, min_conf=0.8)	

	tail_entities=set()
	for item in tail_result:
		if type(item)==tuple:
			tail_entities.add(item[1])

	if len(head_entities)==0 or len(tail_entities)==0:
		return 0		

	avg_score=0.0

	for head_entity in head_entities:
		for tail_entity in tail_entities:
			avg_score=avg_score+dxtr.relatedness(head_entity,tail_entity)

	avg_score=avg_score/(len(head_entities)*len(tail_entities))
	
	# avg_score=np.tanh(avg_score)
	
	if avg_score>=0.5:
		return 1

	else:
		return 0

print Entity_linkage("smithsonian jobs","washington dc")		 			