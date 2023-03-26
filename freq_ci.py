import re
from unicode_tr import unicode_tr

def white_spaced(text):
    # punc = ['.', ',', '!', '?', ':', ';']
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([?,.!"“”;:])', r'\1 \2 ', text)
    return txt

def tr_lower(word):
    w_unicode = unicode_tr(word)
    w_lower = w_unicode.lower()
    return w_lower

def freq_ci_cal(text):
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


