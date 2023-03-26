import re
from collections import Counter
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
    ngrams_freq = Counter(ngrams_list)
    return ngrams_freq

#s_text = "Bu bir deneme metnidir. Deneme metinleri, bir yazılımın doğru ve düzgün çalışıp çalışmadığını test etmek için kullanılır. Bu n-gram örneği bir yazılımın doğru 3'lük grupları hesaplar."
#size = 3
#ngrams_freq = generate_ngrams(s_text, size)
#for ngram, freq in ngrams_freq.items():
#    print(ngram, freq)
