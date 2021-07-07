import bs4 as BS
import textstat
import requests
import spacy 
from spacy.lang.de.examples import sentences 
from collections import Counter
import timeit
import pandas as pd
import enchant
from enchant.checker import SpellChecker

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
    return [sentences, wordCount]
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
    
    #print("Flesch_reading_ease",textstat.flesch_reading_ease(soup))      
    #print("Num syllables:",textSyllable)    
    #print("Num sentences:", textSent)
    #print("Num words:", textWords) 
    dict = {'Metrics' : ['Num syllables', 'Num sentences', 'Num words'],
        'Value' : [textSyllable, textSent, textWords],
        }
    df = pd.DataFrame(dict)
    return df
    #frs = 206.835 - 1.015 *(textWords / textSent) - 84.6 * ( textSyllable / textWords)
    #print( frs )

def syllable_count(wordlist):
    """Calculate syllable in word list or corpus"""

    syllabcount = 0    
    for word in wordlist:
        word = word.lower()
        count = 0
        vowels = "aeiouöäüy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        syllabcount = syllabcount +  count 
        return syllabcount

def gunning_fog_index(words,sent,complexWords):
    """Calculate Gunning Fog Index of corpus"""

    gunIndex = 0.4*((words/sent)+100+(complexWords/words))
    return gunIndex

def lexical_diversity(text):
    return len(set(text)) / len(text)

# percentage
def percentage(count, total):
    return 100 * count / total

def lexicalDiversity(texts):
    """Texical diversity score in percentage """

    lexicalDiversity = [lexical_diversity(text) for text in texts]
    tokens = [len(text) for text in texts]
    types = [len(set(text)) for text in texts]  
    ld = pd.DataFrame({'tokens': tokens, 'types': types,
                    'lexical_diversity': lexicalDiversity})
    ld.sort_values(by='lexical_diversity', ascending=False)
    return lexicalDiversity

def errorCount(text):
    """Calculate Error percentage of the corpous"""

    chkr = SpellChecker("de_DE")
    chkr.set_text(text)
    errorwords = []
    for err in chkr:
    #print ("ERROR:", err.word)
        errorwords.append(err.word)
    return percentage(len(errorwords),len(spacyDataSplit(text)[1]))

start = timeit.timeit()

URL = 'https://www.gevestor.de/finanzwissen/aktien'
soup = webScrapping(URL)

#Manual Split and textstat library used to compare between inital results 
manualSplit(soup)

print("Text Analyse using Textstat Library")
print(textstatDataSplit(soup))

#Using spacy Data for majority of calculations
spacyData =  spacyDataSplit(soup)

gfi = (gunning_fog_index((len(spacyData[1])),len((spacyData[0])),syllable_count(list(soup))))
lexd = (lexicalDiversity([soup]))
erper = (errorCount(soup))
fre =textstat.flesch_reading_ease(soup)
end = timeit.timeit()

print("Time Taken to execute code : ",end - start)

# creating a DataFrame for metrics
dict = {'Metrics' : ['Gunning Fog Index', 'Lexical Diversity', 'Error percent in whole text','Flesch reading ease'],
        'Value' : [gfi, lexd, erper ,fre],
        }
df = pd.DataFrame(dict) 
# displaying the DataFrame
print(df)

#need to do few more matrics calculations 
#gunning fog index need minor changes and validation

