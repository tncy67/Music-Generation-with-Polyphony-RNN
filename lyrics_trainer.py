import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences



# Preprocessed lyrics should be loaded in the variable 'preprocessed_lyrics'
# Load preprocessed lyrics from a file
with open("./generated/preprocessed_lyrics.txt", "r", encoding="utf-8") as f:
    preprocessed_lyrics = [line.strip().split() for line in f]

# Create a Tokenizer and fit on the preprocessed lyrics
tokenizer = Tokenizer()
tokenizer.fit_on_texts(preprocessed_lyrics)
total_words = len(tokenizer.word_index) + 1

# Create input sequences and labels
input_sequences = []
for line in preprocessed_lyrics:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad the input sequences and obtain the predictors and labels
max_sequence_len = max([len(seq) for seq in input_sequences])
# print(input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')
predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
label = to_categorical(label, num_classes=total_words)

# Create the LSTM model
model = Sequential()
model.add(Embedding(total_words, 50, input_length=max_sequence_len - 1))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# Train the LSTM model
model.fit(predictors, label, epochs=100, verbose=1)

# Save the trained model
model.save("./models/lyrics_trainer_model.h5")



