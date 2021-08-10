import bs4 as BS
import requests
import spacy
import time
import pandas as pd
from enchant.checker import SpellChecker
import re
import sys
import csv


def scrap_webpage_to_text(url):
    """Scrapping the web page and returning the text corpus

    Library: Beautiful Soup 4

    Args:
        url (string): Pass the URL of page which need to be scrapped

    Returns:
        scrapped_text (string): webscrapped corpus
    """
    page = requests.get(url)
    soup = BS.BeautifulSoup(page.content, "html.parser")
    soup = list(soup.stripped_strings)
    scrapped_text = " ".join(soup)
    return scrapped_text


def spacy_data_split(soup, language):
    """Using  NLP technique to tokenize words and sentence

    Library: Spacy

    Args:
        soup (string): Text which needs to be processed
        language (string):

    Returns:
        sentence (list): list of sentence
        word (list): list of words
    """

    if language == "de":
        nlp = spacy.load("de_core_news_sm")
    if language == "en":
        nlp = spacy.load("en_core_web_sm")
    about_doc = nlp(soup)
    sentences = list(about_doc.sents)
    wordstrip = re.sub(r"[?|$|.|!]", r"", soup)
    word = wordstrip.split()
    return [sentences, word]


def get_syllable_count(wordlist):
    """Calculate syllable count from given word list
    syllable : A unit of pronunciation having one vowel sound,
            with or without surrounding consonants,
            forming the whole or a part of a word
    Args:
        wordlist (list):

    Returns:
        syllable_count (int): Number of syllable found in total
    """
    syllable_count = 0
    for word in wordlist:
        word = word.lower()
        count = 0
        vowels = "aeiouüöäy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        syllable_count = syllable_count + count
        return syllable_count


def complex_word_list(text, language):
    """Calculate Complex words word using get_syllable_count function

    Args:
        text (string): Corpus from which complex word has to be found
        language (string): Language

    Returns:
        complex_words (list):list of complex words
    """

    complex_words = []
    for word in spacy_data_split(text, language)[1]:
        word = re.sub("es$", "", word)
        word = re.sub("ing$", "", word)
        word = re.sub("ed$", "", word)
        if get_syllable_count([word]) >= 3:
            complex_words.append(word)
    return complex_words


def gunning_fog_index(word_count, sentence_count, complex_words_count):
    """Calculate Gunning Fog Index of corpus
    Refence https://en.wikipedia.org/wiki/Gunning_fog_index

    Args:
        word_count (int): Number of words
        sentence_count (int): Number of sentence
        complex_words_count (int): Number of complex words

    Returns:
        gunning_fog_index_score (float): Gunninng Fog Index calculated Value
    """
    gunning_fog_index_score = 0.4 * (
        (word_count / sentence_count) + (complex_words_count / word_count) * 100
    )
    return gunning_fog_index_score


def lexical_diversity_length(text):
    """Calculate Lexical Diversity of corpus"""

    return len(set(text)) / len(text)


# percentage
def percentage(count, total):
    return 100 * count / total


def lexical_diversity(texts):
    """Texical diversity score in percentage

    Args:
        texts (string): Corpus

    Returns:
        (float): Lexical diversity calculated value
    """

    lexicaldiversity = [lexical_diversity_length(text) for text in texts]
    tokens = [len(text) for text in texts]
    types = [len(set(text)) for text in texts]
    ld = pd.DataFrame(
        {"tokens": tokens, "types": types, "lexical_diversity": lexicaldiversity}
    )
    ld.sort_values(by="lexical_diversity", ascending=False)
    return lexicaldiversity


def error_count(text, language):
    """Calculate Error percentage of the corpous

    Library: enchant

    Args:
        text (string): Corpus which needs to be evaluated
        language (string): Language

    Returns:
        error_percentage (float): Error percentage
    """

    if language == "de":
        chkr = SpellChecker("de_DE")
    if language == "en":
        chkr = SpellChecker("en_US")

    chkr.set_text(text)
    errorwords = []
    for err in chkr:
        errorwords.append(err.word)
    error_percentage = percentage(
        len(errorwords), len(spacy_data_split(text, language)[1])
    )
    return error_percentage


def avgerage_sentence_length(text):
    """Calculate the average sentence length across a corpus

    Args:
        text (string): Text which needs to be processed

    Returns:
       average_sentence_length (float): Average sentence length of corpus
    """

    sentences = text.split(".")
    words = text.split(" ")
    if sentences[len(sentences) - 1] == "":
        average_sentence_length = len(words) / len(sentences) - 1
    else:
        average_sentence_length = len(words) / len(sentences)
    return round(average_sentence_length, 2)


def text_percentage(data, boolfunc):
    """Returns how many % of the 'data' returns 'True' for the given boolfunc."""

    return (sum(1 for x in data if boolfunc(x)) / len(data)) * 100


def flesch_reading_ease(word, sentence, syllable):
    """Calculate flesch reading ease and Flesch reading grade metrics
    Refrence https://simple.wikipedia.org/wiki/Flesch_Reading_Ease

    Args:
        word (int): Number of words
        sentence (int): Number of sentence
        syllable (int): Number of syllable

    Returns:
       flesch_reading_ease_calculate (float): flesch reading ease calculated value
       flesch_reading_ease_grade_calculate (float): flesch reading ease grade calculated value
    """

    flesch_reading_ease_calculate = (
        206.835 - 1.015 * (word / sentence) - 84.6 * (syllable / word)
    )
    flesch_reading_ease_grade_calculate = (
        0.39 * (word / sentence) + 11.8 * (syllable / word) - 15.59
    )
    return flesch_reading_ease_calculate, flesch_reading_ease_grade_calculate


def automated_readablity_score(characters, words, sentences):
    """Calculate readablity of the text formula taken from https://en.wikipedia.org/wiki/Automated_readability_index

    Args:
        characters (int): Number of characters in corpus
        words (int): Number of words in corpus
        sentences (int): Number of sentences in corpus

    Returns:
        auto_readablity_index(float): Automated redablity score calculated value
    """

    auto_readablity_index = (
        4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
    )
    return auto_readablity_index


def grade_check(score):
    """Evalute the average of 3 metrics and give a suitable grade reffered from https://en.wikipedia.org/wiki/Automated_readability_index

    Args:
        score (float): Average score from 3 readblity metrics

    Returns:
        grade (string): Determined Grade
    """

    if score <= 6:
        grade = "Kindergarten"
    elif score <= 7:
        grade = "First/Second Grade"
    elif score <= 9:
        grade = "Third Grade"
    elif score <= 10:
        grade = "Fourth Grade"
    elif score <= 11:
        grade = "Fifth Grade"
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


def csv_reader(filepath):
    """Create a list from csv file

    Args:
        filepath (string): Filepath where csv file is located

    Returns:
        spam_list(list): list of csv file
    """

    spam_list = []
    reader = csv.reader(open(filepath, encoding="utf-8-sig"), delimiter=";")
    for row in reader:
        spam_list.append(row)
    return spam_list[0]


def spam_check(text, spamlist):

    """Check if the string has any spam words from spamlist

    Args:
        text (list): list of words to be checked
        spamlist (list):spam list file as a csv
    Returns:
        wordfound(list): List of words which are found in the spam word list (spamwordlist.csv)
    """

    wordfound = []
    for word in text:
        if word in spamlist:
            wordfound.append(word)
    return wordfound


def analyse_text(soup, language):
    # Using spacy Data for majority of calculations
    spacy_data = spacy_data_split(soup, language)
    spacy_word = spacy_data[1]
    spacy_sentence = spacy_data[0]
    complex_words = complex_word_list(soup, language)
    syllable_count = get_syllable_count(list([soup]))
    character_count = sum(len(i) for i in spacy_data[1])
    gunning_fog_index_result = gunning_fog_index(
        len(spacy_word), len(spacy_sentence), len(complex_words)
    )
    lexical_diversity_result = lexical_diversity([soup])[0]
    error_count_result = error_count(soup, language)
    upper_case_percentage = text_percentage(soup, str.isupper)
    lower_case_percentage = text_percentage(soup, str.islower)
    flesch_reading_ease_result, flesch_reading_ease_index_result = flesch_reading_ease(
        len(spacy_word), len(spacy_sentence), syllable_count
    )
    automate_readablity_score_result = automated_readablity_score(
        character_count, len(spacy_word), len(spacy_sentence)
    )
    average_sentence_length_result = avgerage_sentence_length(soup)  # function call

    # Spamlist checking
    spamlist = csv_reader("spamwordlist.csv")
    spam_check_result = spam_check(spacy_word, spamlist)

    # creating a Dictionary
    metrics_values = {
        "Word Count": len(spacy_word),
        "Sentence Count": len(spacy_sentence),
        "Syllable Count": syllable_count,
        "Complex Words": len(complex_words),
        "Average Sentence length": average_sentence_length_result,
        "Average lower case": lower_case_percentage,
        "Average upper_case_percentage case": upper_case_percentage,
        "Gunning Fog Index": gunning_fog_index_result,
        "Lexical Diversity": lexical_diversity_result,
        "Error percent in whole text": error_count_result,
        "Flesch reading ease": flesch_reading_ease_result,
        "Flesch Kincaid Grade Level": flesch_reading_ease_index_result,
        "Automate readablity score": automate_readablity_score_result,
        "Spam Word List": spam_check_result,
        "Spam Percentage": (len(spam_check_result) / len(spacy_word)),
    }

    # Create the pandas DataFrame from dictionary
    metrics_values_to_df = dfObj = pd.DataFrame(
        list(metrics_values.items()), columns=["Metrics", "Values"]
    )

    print(metrics_values_to_df.round({"Values": 2}))
    # Taking average of 3 metrics to determine difficulty level of the text.
    avgmetrics = (
        gunning_fog_index_result
        + flesch_reading_ease_index_result
        + average_sentence_length_result
    ) / 3
    print(
        "The given text can be read by",
        grade_check(avgmetrics),
        "and Difficulty score is",
        round(avgmetrics, 2),
    )
    return metrics_values_to_df


def main(language, path, url):

    start = time.time()
    # Check for text ,url or text file. Here variable url can be link,a file name or a text string
    if path == "url":
        soup = scrap_webpage_to_text(url)
    if path == "file":
        f = open(url, "r")
        soup = f.read()
    if path == "text":
        soup = url

    language = language.lower()

    # Execute all metric function
    metrics_data_frame = analyse_text(soup, language)

    # displaying the DataFrame
    print("\nAdditional readings \n", metrics_data_frame)

    end = time.time()
    print("Time Taken to execute code : ", end - start)


# Calling main function where arguments are passed
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
