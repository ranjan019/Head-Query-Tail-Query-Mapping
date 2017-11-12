import numpy
import sys
import os
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pdb

head_shape = 5
tail_shape = 10
top_words = 100000
EMBEDDING_DIM = 100
GLOVE_DIR = '../../glove6B'
# word_index = 0

def createEmbeddingMatrix(file_path):
    embeddings_index = {}
    f = open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    text = []
    head = []
    tail = []
    with open(file_path,'r') as f:
        for l in f:
            t = l.split('||')
            text.append(l)
            head.append(t[0].strip())
            tail.append(t[1].strip())
            labels.append(int(t[3].strip()))

    tokenizer = Tokenizer(num_words=top_words)
    tokenizer.fit_on_texts(text)
    sequences_head = tokenizer.texts_to_sequences(head)
    sequences_tail = tokenizer.texts_to_sequences(tail)
    head_data = pad_sequences(sequences_head,maxlen=head_shape)
    tail_data = pad_sequences(sequences_tail,maxlen=tail_shape)
    word_index = tokenizer.word_index
    print "Total Words found : ",len(word_index)
    num_words = min(top_words, len(word_index))
    embedding_matrix = np.zeros((num_words+1, EMBEDDING_DIM))
    for word, i in word_index.items():
        if i >= top_words:
            continue
        embedding_vector = embeddings_index.get(word)
        pdb.set_trace()
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return tokenizer,embedding_matrix,head_data,tail_data,labels,word_index

def model_LSTM_Classifier(head_data,tail_data,labels,embedding_matrix):
    main_input_head = Input(shape=(head_shape,), dtype='int32')
    main_input_tail = Input(shape=(tail_shape,), dtype='int32')

    embedding_layer = Embedding(len(word_index) + 1,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

    x_head = embedding_layer(main_input_head)
    x_tail = embedding_layer(main_input_tail)
    # x_head = Embedding(EMBEDDING_DIM, weights=[embedding_matrix] ,input_dim=top_words, input_length=head_shape)(main_input_head,trainable=False)
    # x_tail = Embedding(EMBEDDING_DIM, weights=[embedding_matrix] ,input_dim=top_words, input_length=tail_shape)(main_input_tail,trainable=False)
    lstm_head = LSTM(100)(x_head)
    lstm_tail = LSTM(100)(x_tail)

    combined_input = keras.layers.concatenate([lstm_head, lstm_tail])
    combined_input = Dense(50, activation='relu')(combined_input)

    main_output = Dense(1, activation='sigmoid')(combined_input)

    model = Model(inputs=[main_input_head, main_input_tail], outputs=[main_output])
    model.compile(optimizer='rmsprop', loss='binary_crossentropy',loss_weights=[1.])

    model.fit([head_data, tail_data], [labels],
              epochs=50, batch_size=32,verbose=1,validation_split=0.2,
              shuffle=True,)

    return model

if __name__== "__main__":
    file_path = sys.argv[1]
    tokenizer,embedding_matrix,head_data,tail_data,,word_index = createEmbeddingMatrix(file_path)
    # for i in range(len(head_data)):
    #     print head_data[i],tail_data[i]
    model = model_LSTM_Classifier(head_data,tail_data,labels,embedding_matrix,word_index)
    model.predict()
