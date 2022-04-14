import re

def turk_lower(word):
    word = word.replace("İ", "i")
    word = word.replace("I", "ı")
    return word.lower()

def white_spaced(text):
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([?,.!"“”;:])', r'\1 \2 ', text)
    return txt

def gen_ngram(text, size):
    ngrams_list = []
    tokens = white_spaced(turk_lower(text))
    tokens = re.sub(r" {2,}", " ", tokens)
    tokens = re.sub(r"\t{1,}", " ", tokens)
    tokens = re.sub(r"\n{1,}", " ", tokens)
    tokens = re.sub(r"\r{1,}", " ", tokens)
    text = turk_lower(white_spaced(tokens).replace("\n", " ")).strip(" ").split()
    for num in range(0, len(text)):
        ngram = text[num:num + size]
        ngrams_list.append(ngram)
    return ngrams_list[:-(size-1)]