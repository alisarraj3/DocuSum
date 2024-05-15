import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict
import numpy as np
import PyPDF2
import io

nlp = spacy.load("en_core_web_sm")

def readPDF(file): 
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

class FileSum:
    def __init__(self, file):
        self.file = file
        self.text = readPDF(file)

    def createSummary(self, num_sentences=3):
        doc = nlp(self.text)
        # Create a list of sentences from the document
        sentences = [sent.text.strip() for sent in doc.sents]
        # Tokenize the document into words
        words = [token.text for token in doc if not token.is_stop and not token.is_punct]
        
        # Construct a word frequency matrix
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word.lower()] += 1

        # Calculate word frequencies
        max_freq = max(word_freq.values())
        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max_freq

        # Construct a sentence score matrix
        sent_scores = defaultdict(int)
        for sent in sentences:
            for word in nlp(sent):
                if word.text.lower() in word_freq:
                    sent_scores[sent] += word_freq[word.text.lower()]


        # Select top N sentences with highest scores
        top_sentences = sorted(sent_scores, key=sent_scores.get, reverse=True)[:num_sentences]

        # Generate the summary
        summary = ' '.join(top_sentences)
        return summary
    
