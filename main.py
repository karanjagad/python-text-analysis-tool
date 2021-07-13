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
import re



def webScrappingold(URL):
    """Using BS4  for scrapping and getting data"""

    page = requests.get(URL)
    soup = BS.BeautifulSoup(page.content,'html.parser').get_text(strip=True)
    return soup


def webScrapping(URL):
    """Using BS4  for scrapping and getting data"""

    page = requests.get(URL)
    soup = BS.BeautifulSoup(page.content,'html.parser')
    soup = list(soup.stripped_strings)
    return ' '.join(soup) 

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
    nlp = spacy.load("en_core_web_sm")
    #nlp = spacy.load("de_core_news_sm")
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
    
    textstat.set_lang('en')
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

def complex_word_list(text):
    """Calculate Complex words word using syllables """
    complexwordlist = []
    for word in spacyDataSplit(text)[1] :
        word = re.sub("es$", "", word)
        word = re.sub("ing$", "", word)
        word = re.sub("ed$", "", word)

        #print(word,":",syllable_count([word]))
        if syllable_count([word]) >= 3:
            complexwordlist.append(word)
            #print(complexwordlist)
    return complexwordlist

def gunning_fog_index(words,sent,complexWords):
    """Calculate Gunning Fog Index of corpus"""
    gunIndex = 0.4*((words/sent)+(complexWords/words)*100)
    return gunIndex

def lexical_diversity(text):
    """Calculate Lexical Diversity of corpus"""
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
    chkr = SpellChecker("en_US")
    #chkr = SpellChecker("de_DE")
    chkr.set_text(text)
    errorwords = []
    for err in chkr:
    #print ("ERROR:", err.word)
        errorwords.append(err.word)
    return percentage(len(errorwords),len(spacyDataSplit(text)[1]))

#function to calculate the average sentence length across a piece of text.
def avg_sentence_len(text):
  sentences = text.split(".") #split the text into a list of sentences.
  words = text.split(" ") #split the input text into a list of separate words
  if(sentences[len(sentences)-1]==""): #if the last value in sentences is an empty string
    average_sentence_length = len(words) / len(sentences)-1
  else:
    average_sentence_length = len(words) / len(sentences)
  return average_sentence_length #returning avg length of sentence

def text_percentage(data, boolfunc):
    """Returns how many % of the 'data' returns 'True' for the given boolfunc."""
    return (sum(1 for x in data if boolfunc(x)) / len(data))*100

def flesch_reading_ease(word,sent,syllab):
    
    fre= 206.835 - 1.015 * ( word / sent ) - 84.6 * ( syllab / word )
    return fre

def automated_readablity_score(characters,words,sentences) :
    """Calculate readablity score"""
    ari  = 4.71 * (characters/words) + 0.5 * (words/sentences) - 21.43
    return ari




start = timeit.timeit()
#lang = input("Select Language Input De for German or En for English ")

#changelanguage(lang)

URL = 'https://www.vnrag.de/about-vnr/'
soup = webScrapping(URL)
soup = "About VNR - VNR Verlag für die Deutsche Wirtschaft AG info@vnr.de Kundenservice: +49 228 9550-100 Chat Self-Service "
#Manual Split and textstat library used to compare between inital results 
manualSplit(soup)

print("Text Analyse using Textstat Library")
print(textstatDataSplit(soup))

#Using spacy Data for majority of calculations
spacyData =  spacyDataSplit(soup)
spacyword =len(spacyData[1])
spacysent = len(spacyData[0])
complexwords = len(complex_word_list(soup))
syllablecount = syllable_count(list([soup]))
charactercount = sum(len(i) for i in spacyData[1])
gfi = gunning_fog_index(spacyword,spacysent,complexwords)
#gfi = (gunning_fog_index((len(spacyData[1])),len((spacyData[0])),syllable_count(list(soup))))
lexd = (lexicalDiversity([soup]))
erper = (errorCount(soup))
#fre =textstat.flesch_reading_ease(soup)
upper = text_percentage( soup, str.isupper )
lower = text_percentage( soup, str.islower )
fre =flesch_reading_ease(spacyword,spacysent,syllablecount)
ari = automated_readablity_score(charactercount,spacyword,spacysent)


ans = avg_sentence_len(soup) #function call

# creating a DataFrame for metrics
dict = {'Metrics' : ['Word Count','Sentence Count','Syllable Count','Complex Words','Gunning Fog Index', 'Lexical Diversity', 'Error percent in whole text','Flesch reading ease','Automate readablity score','Average Sentence length','Average lower case ', 'Average Upper case'],
        'Value' : [spacyword,spacysent,syllablecount,complexwords,gfi, lexd, erper ,fre,ari,ans,lower,upper],
        }
df = pd.DataFrame(dict) 
# displaying the DataFrame
print(df)
print(soup)
end = timeit.timeit()

print("Time Taken to execute code : ",end - start)
