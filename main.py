#!/usr/bin/python3

# Perform Http Request
import requests
# Randomization of letters
import random
# Pattern matching
import re


URL = "https://fly.wordfinderapi.com/api/search?length={}&dictionary=all_en"


def GenerateWordsFromApi(charLength: int, wordLength: int) -> set:
    """Generates Words from API"""
    formatUrl = URL.format(charLength)
    apiResponse = requests.get(formatUrl).json()
    wordList = [data for data in apiResponse['word_pages']]
    # Filter generated words from dictionary in a list
    wordList = [j['word'] for i in wordList for j in i['word_list']]
    # Next We'll create an empty set to not have repeated words in generated list
    wordSet = set({})
    # Until wordLength is satisfied
    while len(wordSet) != wordLength:
        wordSet.add(random.choices(wordList, k=wordLength))  # Keep calling
    return wordSet


def GenerateWordsFromUrl(charLength: int, wordLength: int) -> list:
    """Generates Words by scraping from a Webpage"""
    # Data for post request to server
    data = [
        ('utf8', '\u2713'),
        ('word_generator_form[number_of_words]', str(wordLength)),
        ('word_generator_form[length]', str(charLength)),
        ('word_generator_form[first_letter]', ''),
        ('word_generator_form[last_letter]', ''),
        ('word_generator_form[word_type][]', ''),
        ('word_generator_form[word_type][]', 'verb'),
        ('word_generator_form[word_type][]', 'adjective'),
        ('commit', 'Generate Words'),
    ]
    # Create a post request with data
    response = requests.post('https://word.tips/tools/random-word-generator',
                             data=data, headers={"User-Agent": "Chrome 90.0"}).text
    # Return a list with no whitespaces in string
    return [data.strip() for data in re.findall(r"(?<=<b>)[\sA-z]+", response)]


def main() -> None:
    """Driver Function"""
    charLength = int(input("Enter no. of letters: "))
    wordLength = int(input("Enter no. of words: "))

    # ch = input("1. From API\n2. From WebPage (Recommended)\n\nChoice: ")
    # if ch == 1:
    #     result = GenerateWordsFromApi(charLength, wordLength)
    # else:

    result = GenerateWordsFromUrl(charLength, wordLength)
    # Making sure all words are lowercase and output string
    print("-".join([word.lower() for word in result]))


if __name__ == "__main__":
    main()  # Run
