import requests
import re
import random
import config
import logging
import sys
import time

FORMAT = '%(asctime)-15s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO if config.ENABLE_LOGGING else logging.CRITICAL)

logger = logging.getLogger(__name__)

api_url = f'https://{config.WIKI_REGION}.wikipedia.org/w/api.php'
word_regex = r"\b[a-zA-Z]+\b"
finder = re.compile(word_regex)


def get_words(word_count, char_count):
    try_count = 1
    while True:
        time.sleep(1)
        random_wiki_article_id = requests.get(api_url, params={
            'action': 'query',
            'format': 'json',
            'list': 'random',
            'rnnamespace': '0'
        }).json()['query']["random"][0]['id']

        article_text = requests.get(api_url, params={
            'action': 'query',
            'format': 'json',
            'pageids': f'{random_wiki_article_id}',
            'prop': 'extracts',
            'explaintext': True,
            'redirects': '',
            'exlimit': 'max',
            'exsectionformat': 'plain'
        }).json()["query"]["pages"][f"{random_wiki_article_id}"]["extract"]

        raw_words_list = []
        for word in finder.findall(article_text):
            if len(word) >= char_count:
                raw_words_list.append(word.lower())
        words_list = []

        if len(raw_words_list) < word_count:
            logger.info(f"Try number {try_count} - got {len(raw_words_list)} words instead of {word_count}.")
            try_count += 1
            continue
        elif len(raw_words_list) == word_count:
            logger.info("Got it!")
            return raw_words_list
        else:
            logger.info("Got it!")
            for i in range(word_count):
                word = random.choice(raw_words_list)
                words_list.append(word)
                raw_words_list.remove(word)
            return words_list


def main():
    for id, word in enumerate(get_words(config.NUM_OF_WORDS, config.MIN_CHARACTER_COUNT)):
        if (id + 1) % 3 == 0:
            print(word)
        else:
            sys.stdout.write(word + " ")


if __name__ == "__main__":
    main()
