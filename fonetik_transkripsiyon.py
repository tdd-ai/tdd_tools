# -*- coding: utf-8 -*-

import re

def fonetik_analiz(word):
    word = word.replace(" ", "").lower()
    phonetic_map = {
        "c": "dʒ", "y": "j", "v": "ʋ", "a": "α", "ş": "ʃ", "ç": "tʃ", "j": "ʒ",
    }

    analysis = "".join([phonetic_map.get(i, i) for i in word])

    # Applying phonetic rules
    rules = [
        (r'l(?=[αıou])|(?<=[αıou])l', 'ɫ'),
        (r'g(?=[eiöü])|(?<=[eiöü])g', 'ɟ'),
        (r'(?<=[αeıioöuü])ğ(?=[αeıioöuü])', '•'),
        (r'(?<=[^e])ğ', ': '),
        (r'eğ(?=[^αeıioöuü])', 'ej'),
        (r'h(?=[eiöü])', 'ç'),
        (r'(?<=[αıou])h', 'x'),
        (r'ʋ(?=[uüoö])|(?<=[uüoö])ʋ', 'β'),
        (r'f(?=[uüoö])|(?<=[uüoö])f', 'ɸ'),
        (r'k(?=[αıou])', 'kʰ'),
        (r'k(?=[eiöü])', 'cʰ'),
        (r'(?<=[eiöü])n(?=[cɟcʰ])', 'ɲ'),
        (r'(?<=[αıou])n(?=[kgkʰ])', 'ŋ'),
        (r'm(?=[fɸ])', 'ɱ'),
        (r'p(?=[αeıioöuü])', 'pʰ'),
        (r't(?=[αeıioöuü])', 'tʰ'),
        (r'α(?=[mɱnŋɲ])', 'α̃ '),
        (r'(?<=[ɟlcʰ])α(?=[ɟlcʰ])', 'a'),
        (r'o(?=[mɱnŋɲrɾ̥lɫ])', 'ɔ'),
        (r'ı', 'ɯ'),
        (r'ü', 'y'),
        (r'ö', 'ø'),
        (r'ø(?=[mɱnŋɲrɾ̥lɫ])', 'œ'),
        (r'e(?=[mɱnŋɲrɾ̥lɫ])', 'ɛ')
    ]

    for pattern, replacement in rules:
        analysis = re.sub(pattern, replacement, analysis)

    # Specific end of word rules
    if analysis.endswith("h"):
        analysis = re.sub(r'h$', 'ç', analysis)
    if analysis.endswith("r"):
        analysis = re.sub(r'r$', 'ɾ̥', analysis)
    if analysis.endswith("k"):
        analysis = re.sub(r'(?<=[eiöü])k$', 'c', analysis)
    if analysis.endswith("o"):
        analysis = re.sub(r'o$', 'ɔ', analysis)
    if analysis.endswith("ø"):
        analysis = re.sub(r'ø$', 'œ', analysis)

    return analysis.strip()


sentence = "Bu işlerin nasıl olduğunu bilmiyorum"

for w in sentence.split():
    print(fonetik_analiz(w))


