import os
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download("punkt")
nltk.download("stopwords")


def read_lyrics(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lyrics = f.read()
    return lyrics


def preprocess_lyrics(lyrics):
    # Tokenize the words
    tokens = word_tokenize(lyrics)

    # Convert to lowercase and remove punctuation
    tokens = [word.lower() for word in tokens if word.isalnum()]

    # Remove non-integer tokens
    tokens = [token for token in tokens if token.isalpha()]

    # Add custom stop words
    custom_stop_words = {"vote", "votes"}

    # Remove stop words
    stop_words = set(stopwords.words("turkish")) | custom_stop_words
    tokens = [word for word in tokens if word not in stop_words]

    return tokens


lyrics_folder = "lyrics"
preprocessed_lyrics = []

for file_name in os.listdir(lyrics_folder):
    file_path = os.path.join(lyrics_folder, file_name)
    lyrics = read_lyrics(file_path)
    preprocessed_tokens = preprocess_lyrics(lyrics)
    preprocessed_lyrics.append(preprocessed_tokens)

word_counts = Counter()
for tokens in preprocessed_lyrics:
    word_counts.update(tokens)

min_word_freq = 2
filtered_lyrics = []
for tokens in preprocessed_lyrics:
    filtered_lyrics.append(
        [word for word in tokens if word_counts[word] >= min_word_freq]
    )

# print(preprocessed_lyrics)

# output_file = "./generated/preprocessed_lyrics.txt"
output_file = "./generated/filtered_lyrics.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for tokens in filtered_lyrics:
        f.write(" ".join(tokens) + "\n")

print(f"Preprocessed lyrics saved to {output_file}")
