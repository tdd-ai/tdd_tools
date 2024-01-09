import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
from freq import text_freq_cs, text_freq_ci
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

os.environ['MPLCONFIGDIR'] = '/var/www/.cache/matplotlib'


def generate_wordcloud(text, stop_w, case, cmap):
    stop_words = set(stopwords.words('turkish'))
    if stop_w == 'use':
        text_tokens = word_tokenize(text)
        filtered_tokens = [word for word in text_tokens if word not in stop_words]
        text = ' '.join(filtered_tokens)

    # Calculate word frequencies based on case sensitivity parameter
    if case == 'c_ins':
        word_freqs = text_freq_cs(text)
    else:
        word_freqs = text_freq_ci(text)

    # Generate the wordcloud
    word_frequency = word_freqs['word_frequency']
    word_frequency_dict = {word: frequency for word, frequency in word_frequency}

    wordcloud = WordCloud(width=1920,
                          height=1080,
                          min_font_size=14,
                          background_color="#333333",
                          margin=-0,
                          colormap=cmap).generate_from_frequencies(word_frequency_dict)

    plt.figure(figsize=(16, 9))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = buffer.getvalue()
    buffer.close()
    return image_data

