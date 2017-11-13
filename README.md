### Problem Statement
One of the biggest challenges of commercial search engines is how to handle tail queries, or queries that occur very infrequently. Frequent queries, also known as head queries, are easier to handle largely because their intents are evidenced by abundant click-through data (query logs). Tail queries have little historical data to rely on, which makes them difficult to be learned by ranking algorithms.

The goal of this project is to develop a method to map long-tail queries to head queries, such that the performance of the search engine on such queries can be improved.

### Data Processing:
AOL data contained queries along with the urls clicked (click-through data) and the rank of the url on the search page.

We separated the search queries into head queries and tail queries based on their frequency. Queries with frequency greater than equal to 150 were classified into head queries and queries with frequency less than equal to 5 were classified into tail queries.
Each head query - tail query pair was marked relevant (1) if:
The click-through url is same for both the head query and the tail query, and the rank of the url is <= 5 in both the cases.
Otherwise the pair is deemed irrelevant i.e. 0.



### Models:

#### Model 1: Entity Linking (Baseline)

##### Steps:
1. Pydexter is used to find the entities of the two queries.
2. Entity relatedness is used to find the “relatedness” score between each pair of entities in the two queries (cross product) and take average of it.
3. If the average is greater than threshold (0.5 in this case), then the two queries are deemed relevant, else not.
  

#### Model 2: Ensemble (Entity Linking + Cosine Similarity + Semantic Similarity + Jaccard Distance + SVM)

##### Steps:
1. To find out the feature vector for the head-query tail-query pair 4 modules were created.
2. Module 1: Entity linking. Pydexter is used to find the entities of the two queries and jaccard distance between the sets of entities was used to find entity similarity between the two queries.
3. Module 2: Cosine similarity. Word2vec is used find vectors for each word of a query. The average is taken for all words of the query to create a query vector. Cosine is taken between the 2 query vectors to get the cosine similarity score.
4. Module 3: Jaccard Distance between the two queries.
5. Module 4: Semantic similarity. The synsets of the words of the two queries are matched to find the sentence/semantic similarity between the 2 queries.
6. These 4 modules form the query-pair vector.
7. We feed this query pair vector into SVM to train the model.
8. Testing leads to an accuracy of 78%.

#### Model 3: Neural Network based

	In this method we tried two different approaches, one is to take the average of word2vec values of all words in a given query and use a single word2vec for a whole query, whereas in the other model we used LSTM architecture and word embeddings for representing a query where the final length of the head and tail queries are different as in a head query comprised of 5 words whereas the tail query has 10 words representation.

##### 1. Method 1:	
1. First convert each word into its vector form using different models ( tried both pre trained model on google new corpus and also a model which we trained on wikipedia data dump)
2. Resultant vector of a query is calculated by taking the average of all the vectors of the words that are present in that query.
3. Concatenated both the vector representation of head and tail query.
4. Passed to a neural network which has two dense hidden layers.
5. Output is a single node which is a binary classifier.
 

##### Method 2:

1. Since in the last method we are losing the sequential information hence to capture the information we now used LSTM model 2. for both head and tail queries.
3. Size of words in head queries are fixed to 5 whereas it is 10 for tail query.
4. Used word embedding for word to vec conversion. 
5. For each pair of queries we used two different LSTM model one for each head and tail.
6. Output of that LSTM model is then passed to a dense neural net layer.
7. And finally the final output through a single node using binary classifier.


[Technical Report](https://docs.google.com/document/d/1BjJ6nQR7G-vXcZsXCzcsFGGy5h0VvzrPheoKHhgRpf4/edit?usp=sharing)

### User Study:

We made a google form survey to conduct user study judging satisfaction of users with regards to the model.
[Survey Link](https://goo.gl/forms/EMtoE3pf3NaZXcT32)

**The description of the user study.**

"In each section of the form you'll be given a google search query (Q1) and 3 different snapshots of search results follow.

For each of the search result, you have to assess how the search result satisfies the information needs of the query on a scale of 0-5.
0 means completely useless. 5 means that the information need is fulfilled, and you are happy with it.

There are 8 such sections in this form. "

**Analysis link:** [Analysis](https://docs.google.com/document/d/1z0DhYsh5hhhxzttlt9jYHbw3PaMD0k47R1pVLcAS6W0/edit?usp=sharing)

**Highlight of the analysis:**


Original Query (Avg score 0-5)
3.85

NN Model (Avg score 0-5)
2.28

Baseline Model (Avg score 0-5)
2.25


Important links:
1 [Slideshare link:](https://www.slideshare.net/secret/IKVFW8phbBzcWt)
2 [Survey link:](https://goo.gl/forms/EMtoE3pf3NaZXcT32)
3 [Survey Responses link:](https://docs.google.com/spreadsheets/d/10xQFeOT6Iq1QkL_sPx3Hb9juIEgkXPIs9pnkQ0CBDXw/edit?usp=sharing)
4 [User study survey analysis link:](https://docs.google.com/document/d/1z0DhYsh5hhhxzttlt9jYHbw3PaMD0k47R1pVLcAS6W0/edit?usp=sharing)
5 [github project link 1:](https://github.com/ranjan019/Head-Query-Tail-Query-Mapping)
	[github project link 2:](https://github.com/Viditjn/Head-Tail-Query-Mapping)
6 [github project website:](https://ranjan019.github.io/Head-Query-Tail-Query-Mapping/)


