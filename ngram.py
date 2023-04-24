import re
from unicode_tr import unicode_tr

def preprocess(text):
    # Lowercase and remove special characters
    text = unicode_tr(text).lower()
    text = re.sub(r'[^a-zşğıiüöç\n ]', '', text)
    return text

def generate_ngrams(text, size):
    # Tokenize and generate n-grams
    tokens = preprocess(text).strip().split()
    ngrams_list = [tuple(tokens[num:num + size]) for num in range(0, len(tokens) - size + 1)]
    # Count frequencies
    ngrams_freq = {}
    for ngram in ngrams_list:
        if ngram in ngrams_freq:
            ngrams_freq[ngram] += 1
        else:
            ngrams_freq[ngram] = 1
    # Sort by frequency
    sorted_ngrams = dict(sorted(ngrams_freq.items(), key=lambda x: x[1], reverse=True))
    return sorted_ngrams

