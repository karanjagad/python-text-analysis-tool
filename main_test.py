from re import S
from main import *

text = "These are short, gebührenfrei famous texts in English from classic sources like the Bible or Shakespeare. Some texts have word definitions and explanations to help you. Some of these texts are written in an old style of English. Try to understand them, because the English that we speak today is based on what our great, great, great, great grandparents spoke before! Of course, Aktie not all these texts were originally written in English. The Bible, for example, is a translation. But they are all well known in English today, and many of them express beautiful thoughts free."
dataframe_analysed_text = analyse_text(text, "en")
print(dataframe_analysed_text.loc[0].at["Metrics"])


def test_avgerage_sentence_length():
    assert avgerage_sentence_length(text) != 5
    assert avgerage_sentence_length(text) == 12.86


def test_spacy_data_split():
    assert type(spacy_data_split(text, "en")) == list


def test_scrap_webpage_to_text():
    assert (
        type(scrap_webpage_to_text("https://www.gevestor.de/finanzwissen/aktien"))
        == str
    )


def test_spacy_data_split():
    text = "Hello world!"
    assert spacy_data_split(text, "en")[1] == [
        "Hello",
        "world",
    ]
    # assert type(spacy_data_ssplit(text , "en")[1]) == list

    # assert spacy_data_split(text, "en")[0] == "Hello world"


def complex_word_list():
    assert type(complex_word_list(text, "de")) == list
