import bs4 as BS
import textstat
import requests
import spacy 
from spacy.lang.de.examples import sentences 
from collections import Counter


def webScrapping(URL):
    """Using BS4  for scrapping and getting data"""

    page = requests.get(URL)
    soup = BS.BeautifulSoup(page.content,'html.parser').get_text(strip=True)
    return soup

def manualSplit(soup):
    """ Text Analysing using Manual Split"""

    soupSent = soup.split('.')
    soupWord = []
    for word in soupSent:
        soupWord =soupWord + (word.split(' '))
    print("Text Analyse using Manual Split meathod")
    print("Soup sentence",len(soupSent))
    print("soup Word",len(soupWord))

def spacyDataSplit(soup):
    """Text Analysisng  using Spacy library"""

    nlp = spacy.load("de_core_news_sm")
    about_doc = nlp(soup)
    sentences = list(about_doc.sents)
    about_doc = nlp(soup)
    sentences = list(about_doc.sents)
    wordCount = [token.text for token in about_doc]
    print("Text analysisng using spacy ")
    print("Sentence Count", len(sentences))   
    print("Word Count",len(wordCount))

   
def textstatDataSplit(soup):
    """Text Analysisng  using textstat library """
    textstat.set_lang('de')
    your_text = soup
    textSyllable  =  textstat.syllable_count(your_text)
    textSent  = textstat.sentence_count(your_text)
    textWords = textstat.lexicon_count(your_text, removepunct=True)

    print("Text Analyse using Textstat Library")
    print("Flesch_reading_ease",textstat.flesch_reading_ease(soup))      
    print("Num syllables:",textSyllable)    
    print("Num sentences:", textSent)
    print("Num words:", textWords) 

    #frs = 206.835 - 1.015 *(textWords / textSent) - 84.6 * ( textSyllable / textWords)
    #print( frs )



URL = 'https://www.gevestor.de/finanzwissen/aktien'
soup = webScrapping(URL)

manualSplit(soup)
spacyDataSplit(soup)
textstatDataSplit(soup)

#need to do few more matrics calculations 

    






