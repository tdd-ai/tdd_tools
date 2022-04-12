import re

def white_spaced(text):
    # punc = ['.', ',', '!', '?', ':', ';']
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([,.!";:])', r'\1 \2 ', text)
    return txt

def freq_cal(text):
    tokens = white_spaced(text)
    tokens = re.sub(r" {2,}", " ", tokens)
    tokens = re.sub(r"\t{1,}", " ", tokens)
    tokens = tokens.replace("'''", "\"")
    tokens = tokens.replace("''", "\"")
    tokens = tokens.replace("\n", " ").strip(" ")
    word_list = white_spaced(tokens).split(" ")
    freq_dic = {}
    for word in word_list:
        try:
            freq_dic[word] += 1
        except:
            freq_dic[word] = 1
    freq_list = freq_dic.items()
    freq_list2 = [(val, key) for key, val in freq_dic.items()]
    freq_list2.sort(reverse=True)
    resultset = {}
    token_count = len(word_list)
    unique_token = len(freq_dic)
    resultset['input'] = tokens
    words = freq_list2
    ratio = unique_token / token_count
    return token_count, unique_token, ratio, tokens, words


