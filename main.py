#!/usr/bin/python3

import requests
import random, re


# Makes a GET request and return json from api
def GetRequest(url) -> dict:
    return requests.get(url).text


URL = "https://fly.wordfinderapi.com/api/search?length={}&dictionary=all_en"


def GenerateWordsFromApi(charLength: int, wordLength: int):
    formatUrl = URL.format(charLength)
    apiResponse = GetRequest(formatUrl)
    wordList = [data for data in apiResponse['word_pages']]
    wordList = [j['word'] for i in wordList for j in i['word_list']]
    wordSet = set({})
    while len(wordSet) != wordLength:
        wordSet = set(random.choices(wordList, k=wordLength))
    return wordSet


def GenerateWordsFromUrl(charLength: int, wordLength: int):
    data = [
        ('utf8', '\u2713'),
        ('word_generator_form[number_of_words]', str(wordLength)),
        ('word_generator_form[length]', str(charLength)),
        ('word_generator_form[first_letter]', ''),
        ('word_generator_form[last_letter]', ''),
        ('word_generator_form[word_type][]', 'noun'),
        ('word_generator_form[word_type][]', 'verb'),
        ('word_generator_form[word_type][]', 'adjective'),
        ('commit', 'Generate Words'),
    ]

    response = requests.post('https://word.tips/tools/random-word-generator', data=data, headers={"User-Agent": "Chrome 90.0"}).text
    return [data.strip() for data in re.findall(r"(?<=<b>)[\sA-z]+", response)]


def main():
    charLength = int(input("Enter no. of letters: "))
    wordLength = int(input("Enter no. of words: "))
    ch = input("1. From API\n2. From WebPage\n\nChoice: ")
    if ch == 1:
        result = GenerateWordsFromApi(charLength, wordLength)
    else:
        result = GenerateWordsFromUrl(charLength, wordLength)
    print("-".join([word.lower() for word in result]))


if __name__ == "__main__":
    main()
