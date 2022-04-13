import re

def turk_lower(word):
    word = word.replace("İ", "i")
    word = word.replace("I", "ı")
    return word.lower()

def white_spaced(text):
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([,.!"“”;:])', r'\1 \2 ', text)
    return txt

def gen_ngram(text, size):
    ngrams_list = []
    text = turk_lower(white_spaced(text).replace("  ", " ").replace("\n", "")).strip(" ").split(" ")
    for num in range(0, len(text)):
        ngram = text[num:num + size]
        ngrams_list.append(ngram)
    return ngrams_list[:-(size-1)]