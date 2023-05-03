import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os


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

def generate_text(seed_text, next_words, model, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break

        seed_text += " " + output_word

    return seed_text


from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("./models/lyrics_trainer_model.h5", compile=False)

# Generate new lyrics
seed_text = "senden sonra ne başkası"   
next_words = 50
generated_lyrics = generate_text(seed_text, next_words, model, max_sequence_len)
# print(generated_lyrics)

# Replace spaces with underscores and append the .txt extension
output_file_name = seed_text.replace(" ", "_") + ".txt"

# Make sure the generated folder exists
os.makedirs("./generated_lyrics", exist_ok=True)

output_file = os.path.join("./generated_lyrics/", output_file_name)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(generated_lyrics)

print(f"Generated lyrics saved to {output_file}")

