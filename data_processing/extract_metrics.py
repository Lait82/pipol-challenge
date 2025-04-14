from collections import Counter
from scraping.article import Article
import pandas as pd
from collections import Counter
import re
from .transformers import *

def extract_metrics_from_articles(articles: list[Article]) -> tuple[pd.DataFrame | None]:
    char_counter = Counter({})
    word_counter = Counter({})
    capitalized_words = []

    for a in articles:
        title = a.title
        if title is None:
            continue

        char_counter.update(list(title))
        words = re.findall(r'\b\w+\b', title.lower())
        word_counter.update(words)
        capitalized_words.extend([w for w in title.split() if w.istitle()])
    
    # Convert to DataFrame
    capitalized_words = list(set(capitalized_words))

    capitalized_words = list_to_df(capitalized_words, 'word')
    word_counter_df = counter_to_df(word_counter, 'word')
    char_counter_df = counter_to_df(char_counter, 'character')

    return word_counter_df, char_counter_df, capitalized_words 
