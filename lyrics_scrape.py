import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def get_lyrics_links(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, "html.parser")
    song_links = soup.select(".list-line.margint10.clearfix > a")
    return [urljoin(main_url, link["href"]) for link in song_links]

def replace_turkish_characters(text):
    # turkish_characters = "IıİÖÜöüÇĞŞçğş"
    # english_characters = "liIOUouCGScgs"
    turkish_characters = "I"
    correct_characters = "l"
    translation_table = str.maketrans(turkish_characters, correct_characters)
    return text.translate(translation_table)

def get_lyrics(lyrics_url):
    response = requests.get(lyrics_url)
    soup = BeautifulSoup(response.content, "html.parser")
    lyrics_div = soup.find("div", class_="lyric-text margint20 marginb20")
    
    if lyrics_div:
        text = lyrics_div.get_text(separator=" ").strip()   
        return replace_turkish_characters(text=text)      
    else:
        return None

def get_song_titles(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, "html.parser")
    song_titles = soup.select(".list-line.margint10.clearfix > a")
    return [title.text.strip() for title in song_titles]

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).replace("/", "-").rstrip()

main_url = "https://www.sarkisozlerihd.com/sarkici/sezen-aksu/"
lyrics_links = get_lyrics_links(main_url)
song_titles = get_song_titles(main_url)

os.makedirs("lyrics", exist_ok=True)

for title, link in zip(song_titles, lyrics_links):
    lyrics = get_lyrics(link)
    if lyrics:
        sanitized_title = sanitize_filename(title)
        with open(f"lyrics/{sanitized_title}.txt", "w", encoding="utf-8") as f:
            f.write(lyrics)
        print(f"Saved lyrics for '{title}' in 'lyrics/{sanitized_title}.txt'")
    else:
        print(f"Error: Could not find lyrics for '{title}'")
