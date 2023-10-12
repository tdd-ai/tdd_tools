import re
from collections import defaultdict
from unicode_tr import unicode_tr

def white_spaced(text):
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ.])([?,.!"“”;:])', r'\1 \2 ', text)
    return txt

def tr_lower(word):
    w_unicode = unicode_tr(word)
    w_lower = w_unicode.lower()
    return w_lower

def text_freq_ci(text):
    tokens = white_spaced(text)
    tokens = re.sub(r"\s+", " ", tokens)
    tokens = tokens.replace("'''", "\"")
    tokens = tokens.replace("''", "\"")
    tokens = tokens.translate(str.maketrans('', '', "“”"))
    tokens = tokens.replace("\n", " ")
    tokens = tokens.strip()
    word_list = white_spaced(tokens).split()
    freq_dic = defaultdict(int)
    for word in word_list:
        freq_dic[word] += 1
    words = sorted(freq_dic.items(), key=lambda x: x[1], reverse=True)
    token_count = len(word_list)
    unique_token = len(freq_dic)
    ratio = unique_token / token_count
    resultset = {
        'input': tokens,
        'word_count': token_count,
        'unique_count': unique_token,
        'word_frequency': words,
        'type_token_ratio': ratio
    }
    return resultset

def text_freq_cs(text):
    tokens = white_spaced(text)
    tokens = re.sub(r"\s+", " ", tokens)
    tokens = tokens.replace("'''", "\"")
    tokens = tokens.replace("''", "\"")
    tokens = tokens.translate(str.maketrans('', '', "“”"))
    tokens = tokens.replace("\n", " ")
    tokens = tokens.strip()
    word_list = white_spaced(tr_lower(tokens)).split()
    freq_dic = defaultdict(int)
    for word in word_list:
        freq_dic[word] += 1
    words = sorted(freq_dic.items(), key=lambda x: x[1], reverse=True)
    token_count = len(word_list)
    unique_token = len(freq_dic)
    ratio = unique_token / token_count
    resultset = {
        'input': tokens,
        'word_count': token_count,
        'unique_count': unique_token,
        'word_frequency': words,
        'type_token_ratio': ratio
    }
    return resultset

def showFrequencies(w_order, w_list):
    new_word_order = {}
    for i, word in w_order.items():
        if isinstance(word, tuple):
            new_word_order[i] = (word[0], word[1], w_list.get(word[0]))
        else:
            new_word_order[i] = (word, w_list.get(word))
    return new_word_order

def convert_to_html(new_word_order):
    html_str = ""
    for i, item in new_word_order.items():
        word = item[0]
        freq = item[1]
        html_str += f"{word}<sup><span class='badge badge-pill badge-warning' onclick=\"this.classList.toggle('selected')\">{freq}</span></sup>"
    return html_str

