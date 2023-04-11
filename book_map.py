import os
import fitz
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict

import os
import fitz
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict

import os
import fitz
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict

def summarize_and_map(file_path, bullet_points=True, font_size=16):
    # Extract text from PDF file
    with fitz.open(file_path) as doc:
        text = ''
        for page in doc:
            text += page.get_text()

    # Summarize text using TextRank algorithm
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    sentences = [sent for sent in doc.sents if len(sent) > 10]
    phrase_scores = defaultdict(int)
    for phrase in doc.noun_chunks:
        if len(phrase) > 1 and phrase.text.lower() not in STOP_WORDS:
            phrase_scores[phrase.text] += phrase.root.dep_ in {'nsubj', 'dobj', 'pobj'}
    sentence_scores = defaultdict(int)
    for sent in sentences:
        for phrase in sent.noun_chunks:
            if phrase.text in phrase_scores:
                sentence_scores[sent] += phrase_scores[phrase.text]
    summary = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:5]

    # Create mind map as HTML file
    title = os.path.splitext(os.path.basename(file_path))[0]
    mind_map = f'<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n<style>\nbody {{ font-family: Arial, sans-serif; font-size: {font_size}px; }}\nul {{ list-style: {"disc" if bullet_points else "none"}; padding-left: {"30px" if bullet_points else "0px"}; }}\n.topic {{ font-size: {font_size*1.5}px; font-weight: bold; color: #414a4c; }}\n.sent {{ margin-left: {"30px" if bullet_points else "0px"}; }}\n</style>\n</head>\n<body>\n<h1><center>{title}</center></h1>\n'
    topics = defaultdict(list)
    for sentence in summary:
        topic = sentence.root.text.capitalize()
        if topic not in topics:
            topics[topic].append(sentence)
        else:
            topics[topic].append(sentence)
    for topic, sentences in topics.items():
        mind_map += f'<h2 class="topic">{topic}</h2>\n<ul>\n'
        for sent in sentences:
            mind_map += f'<li class="sent">{sent}</li>\n'
        mind_map += '</ul>\n'

    mind_map += '</body>\n</html>\n'

    # Save mind map as HTML file
    with open(f'{title}.html', 'w', encoding='utf-8') as f:
        f.write(mind_map)
    print(f'Mind map saved to {os.getcwd()}\\{title}.html')




if __name__ == '__main__':
    file_path = input('Enter file path: ')
    map_size = int(input('Enter maximum summary size (in sentences): '))
    summarize_and_map(file_path, map_size)
