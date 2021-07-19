import bs4 as BS
import textstat
import requests
import spacy
from spacy.lang.de.examples import sentences
from collections import Counter
import time
import pandas as pd
from enchant.checker import SpellChecker
import re
import sys


def web_scrapping(URL):
    """Using BS4  for scrapping and getting data"""

    page = requests.get(URL)
    soup = BS.BeautifulSoup(page.content, "html.parser")
    soup = list(soup.stripped_strings)
    return " ".join(soup)


def spacy_data_split(soup, lang):
    """Text Analysisng  using Spacy library"""

    if lang == "de":
        nlp = spacy.load("de_core_news_sm")
    if lang == "en":
        nlp = spacy.load("en_core_web_sm")
    about_doc = nlp(soup)
    sentences = list(about_doc.sents)
    about_doc = nlp(soup)
    sentences = list(about_doc.sents)
    wordstrip = re.sub(r"[?|$|.|!]", r"", soup)
    word = wordstrip.split()
    return [sentences, word]


def syllable_count(wordlist):
    """Calculate syllable in word list or corpus"""

    syllabcount = 0
    for word in wordlist:
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        syllabcount = syllabcount + count
        return syllabcount


def complex_word_list(text, lang):
    """Calculate Complex words word using syllables"""

    complexwordlist = []
    for word in spacy_data_split(text, lang)[1]:
        word = re.sub("es$", "", word)
        word = re.sub("ing$", "", word)
        word = re.sub("ed$", "", word)
        if syllable_count([word]) >= 3:
            complexwordlist.append(word)
    return complexwordlist


def gunning_fog_index(words, sent, complexWords):
    """Calculate Gunning Fog Index of corpus"""

    gunIndex = 0.4 * ((words / sent) + (complexWords / words) * 100)
    return gunIndex


def lexical_diversity(text):
    """Calculate Lexical Diversity of corpus"""

    return len(set(text)) / len(text)


# percentage
def percentage(count, total):
    return 100 * count / total


def lexicaldiversity(texts):
    """Texical diversity score in percentage"""

    lexicaldiversity = [lexical_diversity(text) for text in texts]
    tokens = [len(text) for text in texts]
    types = [len(set(text)) for text in texts]
    ld = pd.DataFrame(
        {"tokens": tokens, "types": types, "lexical_diversity": lexicaldiversity}
    )
    ld.sort_values(by="lexical_diversity", ascending=False)
    return lexicaldiversity


def errorCount(text, lang):
    """Calculate Error percentage of the corpous"""

    if lang == "de":
        chkr = SpellChecker("de_DE")
    if lang == "en":
        chkr = SpellChecker("en_US")

    chkr.set_text(text)
    errorwords = []
    for err in chkr:
        errorwords.append(err.word)
    return percentage(len(errorwords), len(spacy_data_split(text, lang)[1]))


def avg_sentence_len(text):
    """Calculate the average sentence length across a piece of text."""

    sentences = text.split(".")
    words = text.split(" ")
    if sentences[len(sentences) - 1] == "":
        average_sentence_length = len(words) / len(sentences) - 1
    else:
        average_sentence_length = len(words) / len(sentences)
    return average_sentence_length


def text_percentage(data, boolfunc):
    """Returns how many % of the 'data' returns 'True' for the given boolfunc."""

    return (sum(1 for x in data if boolfunc(x)) / len(data)) * 100


def flesch_reading_ease(word, sent, syllab):
    """Calculate flesch reading easy metrics formula taken from https://simple.wikipedia.org/wiki/Flesch_Reading_Ease"""

    fre = 206.835 - 1.015 * (word / sent) - 84.6 * (syllab / word)
    freg = 0.39 * (word / sent) + 11.8 * (syllab / word) - 15.59
    return fre, freg


def automated_readablity_score(characters, words, sentences):
    """Calculate readablity of the text formula taken from  https://en.wikipedia.org/wiki/Automated_readability_index"""

    ari = 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
    return ari


def grade_check(score):
    """Evalute the average of 3 metrics and give a suitable grade reffered from https://en.wikipedia.org/wiki/Automated_readability_index"""

    if score <= 6:
        grade = "Kindergarten"
    elif score <= 7:
        grade = "First/Second Grade"
    elif score <= 9:
        grade = "Third Grade"
    elif score <= 10:
        grade = "Fourth Grade"
    elif score <= 11:
        grade = "Fifth Grade "
    elif score <= 12:
        grade = "Sixth Grade"
    elif score <= 13:
        grade = "Seventh Grade"
    elif score <= 14:
        grade = "Eighth Grade"
    elif score <= 15:
        grade = "Ninth Grade"
    elif score <= 16:
        grade = "Tenth Grade"
    elif score <= 17:
        grade = "Eleventh Grade"
    elif score <= 18:
        grade = "Twelfth grade"
    elif score <= 24:
        grade = "College student"
    elif score >= 24:
        grade = "Twelfth grade"

    return grade


def main(lang, path, url):
    start = time.time()
    if path == "url":
        soup = web_scrapping(url)
    if path == "text":
        f = open(url, "r")
        soup = f.read()
    lang = lang.lower()

    # Using spacy Data for majority of calculations
    spacydata = spacy_data_split(soup, lang)
    spacyword = len(spacydata[1])
    spacysent = len(spacydata[0])
    complexwords = len(complex_word_list(soup, lang))
    syllablecount = syllable_count(list([soup]))
    charactercount = sum(len(i) for i in spacydata[1])
    gfi = gunning_fog_index(spacyword, spacysent, complexwords)
    lexd = lexicaldiversity([soup])
    erper = errorCount(soup, lang)
    upper = text_percentage(soup, str.isupper)
    lower = text_percentage(soup, str.islower)
    fre, freg = flesch_reading_ease(spacyword, spacysent, syllablecount)
    ari = automated_readablity_score(charactercount, spacyword, spacysent)
    ans = avg_sentence_len(soup)  # function call

    # creating a DataFrame for metrics
    dict = {
        "Metrics": [
            "Word Count",
            "Sentence Count",
            "Syllable Count",
            "Complex Words",
            "Average Sentence length",
            "Average lower case ",
            "Average Upper case",
            "Gunning Fog Index",
            "Lexical Diversity",
            "Error percent in whole text",
            "Flesch reading ease",
            "Flesch Kincaid Grade Level",
            "Automate readablity score",
        ],
        "Value": [
            spacyword,
            spacysent,
            syllablecount,
            complexwords,
            ans,
            lower,
            upper,
            gfi,
            lexd,
            erper,
            fre,
            freg,
            ari,
        ],
    }
    df = pd.DataFrame(dict)

    # Taking average of 3 metrics to determine difficulty level of the text.
    avgmetrics = (gfi + freg + ari) / 3
    print(
        "The given text can be read by",
        grade_check(avgmetrics),
        "and Difficulty score is",
        round(avgmetrics, 2),
    )

    print("Additional readings")

    # displaying the DataFrame
    print(df)

    end = time.time()
    print("Time Taken to execute code : ", end - start)


# Calling main function where arguments are passed
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
