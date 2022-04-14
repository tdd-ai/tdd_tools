from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
import re
from deascii import Deasciifier
from freq_ci import freq_ci_cal
from freq import freq_cal
from list_in_text import check
from ngram import gen_ngram

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/deascii')
def deasci():
    return render_template('/deascii.html')

@app.route('/deascii', methods=['POST'])
def deasci_post():
    if request.method == 'POST':
        word = request.form['word']
        if len(word) == 0:
            return render_template("no_input.html", error="No Input!!!")
        deasciifier = Deasciifier(word)
        my_deasciified_turkish_txt = deasciifier.convert_to_turkish()
        return render_template("deascii.html", my_deasciified_turkish_txt = my_deasciified_turkish_txt, word = word)
    else:
        return render_template("404.html", error="No Input!!!")

@app.route('/freq')
def freq():
    return render_template('/freq.html')

@app.route('/freq', methods=['POST'])
def freq_post():
    if request.method == 'POST':
        word = request.form['word']
        freqed = freq_cal(word.replace("\n", " ").rstrip(" "))
        num_of_tokens = freqed[0]
        num_unique_tokens = freqed[1]
        ttr = "%.3f" % round(freqed[2], 2)
        freq_list = []
        for item in freqed[4]:
            freq_list.append(item)
        if len(freq_list) <= 25:
            top_25 = freq_list
        else:
            top_25 = freq_list[:25]
        return render_template("freq.html",
                               word=word,
                               freqed=freqed[4],
                               num_of_tokens=num_of_tokens,
                               num_unique_tokens=num_unique_tokens,
                               ttr=ttr,
                               freq_list=freq_list,
                               top_25=top_25)


@app.route('/freq_ci')
def freq_ci():
    return render_template('/freq_ci.html')

@app.route('/freq_ci', methods=['POST'])
def freq_ci_post():
    if request.method == 'POST':
        word = request.form['word']
        freqed_ci = freq_ci_cal(word.replace("\n", " ").rstrip(" "))
        num_of_tokens = freqed_ci[0]
        num_unique_tokens = freqed_ci[1]
        ttr = "%.3f" % round(freqed_ci[2], 2)
        freq_list = []
        for item in freqed_ci[4]:
            freq_list.append(item)
        if len(freq_list) <= 25:
            top_25 = freq_list
        else:
            top_25 = freq_list[:25]
        return render_template("freq_ci.html",
                               word=word,
                               freqed_ci=freqed_ci,
                               num_of_tokens=num_of_tokens,
                               num_unique_tokens=num_unique_tokens,
                               ttr=ttr,
                               freq_list=freq_list,
                               top_25=top_25)


@app.route('/list_check')
def list_control():
    return render_template('/list_check.html')

@app.route('/list_check', methods=['POST'])
def list_check():
    if request.method == 'POST':
        girdi_metin = request.form['text_input']
        word_list = request.form['liste']
        word_list = word_list.replace("\n", " ").strip(" ")
        matches = check(girdi_metin, word_list)[0]
        misses = check(girdi_metin, word_list)[1]
        return render_template("list_check.html",
                               word_list=word_list,
                               girdi_metin=girdi_metin,
                               matches=matches,
                               misses=misses
                               )

@app.route('/ngram')
def ngram():
    return render_template('/ngram.html')

@app.route('/ngram', methods=['POST'])
def ngram_calculation():
    if request.method == 'POST':
        girdi_metin = request.form['text_input']
        n_span = int(request.form['ngram_span'])
        ngrams = gen_ngram(girdi_metin,n_span)
        num_of_ngrams = len(ngrams)
        return render_template("ngram.html",
                            num_of_ngrams=num_of_ngrams,
                            ngram_input=girdi_metin,
                            ngrams=ngrams)


if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.run(port=5000, use_reloader=True)
