def entity_check(headQuery,tailQuery,dxtr):

	# getting entites in the head query
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


	# print tail_entities

	# getting the common entities
	common_entites=head_entities.intersection(tail_entities)
	# print common_entites

	entity_score= float(len(common_entites))/(len(head_entities)+len(tail_entities)-len(common_entites))
	return entity_score


# entity_check("Dexter is an American television series","Comedy Central is an American television channel")	