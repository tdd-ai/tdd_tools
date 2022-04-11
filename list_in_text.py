def turk_lower(word):
    word = word.replace("İ", "i")
    word = word.replace("I", "ı")
    return word.lower()

def white_spaced(text):
    # punc = ['.', ',', '!', '?', ':', ';']
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([,.!";:])', r'\1 \2 ', text)
    return txt


def check(metin,liste):
    var_list = []
    yok_list = []
    metin = [turk_lower(w) for w in metin.split(" ")]
    liste = [turk_lower(w) for w in liste.split(" ")]
    for word in liste:
        if word in metin:
            var_list.append(word)
        if word not in metin:
            yok_list.append(word)
    return var_list, yok_list

def counts(liste):
    sayim = [[x, liste.count(x)] for x in set(liste)]
    return liste