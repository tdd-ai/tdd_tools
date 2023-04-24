from flask import Flask, jsonify, request, render_template, Response, redirect, url_for, session, flash
import matplotlib.pyplot as plt
from deascii import Deasciifier
from word_cloud import generate_wordcloud
from freq import text_freq_cs, text_freq_ci, tr_lower, showFrequencies, convert_to_html
import matplotlib.pyplot as plt
from io import BytesIO
from wordcloud import WordCloud
from ngram import generate_ngrams
import json
from difflib import  ndiff
import base64
from base64 import b64encode
from jinja2 import Environment

env = Environment()
env.filters['b64encode'] = b64encode

app = Flask(__name__)
app.secret_key = 'top_secret_key' # Set a secret key for your app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/deascii_input', methods=['POST', 'GET'])
def deascii_input():
    if request.method == 'POST':
        form_data = request.form
        in_text = form_data.get('in_text')
        session['in_text'] = in_text
        return redirect(url_for('deasci_post'))
    return render_template('/deascii_input.html')


@app.route('/deascii_out', methods=['POST', 'GET'])
def deasci_post():
    # Retrieve input text from session
    in_text = session.get('in_text')

    # Deasciify input text
    deasciifier = Deasciifier(in_text)
    deasciified_turkish_txt = deasciifier.convert_to_turkish()

    # Get list of differences between original and deasciified texts
    differences = list(ndiff(in_text, deasciified_turkish_txt))
    # Create a dictionary of characters that have changed between the two strings
    changed_chars = {'c': 'ç', 'C': 'Ç', 'g': 'Ğ', 'g': 'ğ', 'o': 'ö', 'O': 'Ö', 'U': 'Ü', 'u': 'Ü', 'i': 'ı', 'I': 'İ',
                     's': 'Ş', 's': 'Ş'}
    html = ''
    # Iterate over differences and replace characters as necessary
    for diff in differences:
        if diff.startswith('- '):
            pass
        elif diff.startswith('+ '):
            char = diff[2:]
            new_char = changed_chars.get(char, char)
            html += f'<span style="color:red">{new_char}</span>'
        else:
            html += diff[2:]


    # Pass the input text, deasciified text, and differences to the HTML template
    return render_template("deascii_output.html", in_text=in_text, deasciified_turkish_txt=deasciified_turkish_txt, html=html)

@app.route('/freq_input', methods=['POST', 'GET'])
def freq_input():
    if request.method == 'POST':
        case = request.form['case']
        in_text = request.form['in_text']
        if len(in_text) == 0:
            flash("No input provided")
            return render_template('/freq_input.html')
        return redirect(url_for('freq_post', case=case, in_text=in_text))
    return render_template('/freq_input.html')

@app.route('/freq', methods=['POST', 'GET'])
def freq_post():
    word = request.args.get('in_text')
    case = request.args.get('case', 'ins') # use get method with a default value
    if case == "ins":
        word_freqs = text_freq_ci(word)
    elif case == "s":
        word_freqs = text_freq_cs(word)
    tokens = word_freqs['input']
    token_count = word_freqs['word_count']
    unique_token = word_freqs['unique_count']
    words = word_freqs['word_frequency']
    ratio = '%.3f'%(word_freqs['type_token_ratio'])
    word_list = {key: value for key, value in words}
    # Show input text with freqs
    w_list = [(i, tr_lower(t)) for i, t in enumerate(tokens.split())]
    word_order = {t[0]: t[1] for t in w_list}
    new_word_order = showFrequencies(word_order, word_list)
    x = convert_to_html(new_word_order)
    # Convert freq to download object
    export_list = json.dumps(word_list)
    # Create graph
    top_words = sorted(word_list.items(), key=lambda x: x[1], reverse=True)[:50]
    # Compute the ranks and frequencies of the top words
    ranks = list(range(1, len(top_words) + 1))
    frequencies = [count for word, count in top_words]
    # Plot the frequencies against the ranks on a log-log scale
    fig, ax = plt.subplots(figsize=(21, 7))
    ax.loglog(ranks, frequencies, marker='*')
    ax.set_title('Zipf\'s Law - Top 50')
    ax.set_xlabel('Rank')
    ax.set_ylabel('Frequency')
    # Save the plot to a buffer as a PNG image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Encode the plot bytes as a base64 string
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    return render_template("freq_output.html", x=x, plot_data=plot_data, new_word_order= new_word_order, tokens=tokens, token_count=token_count, unique_token=unique_token, words=words, ratio=ratio, export_list=export_list)


@app.route('/ngram_input', methods=['POST', 'GET'])
def ngram_input():
    if request.method == 'POST':
        nspan = request.form['nspan']
        in_text = request.form['in_text']
        if len(in_text) == 0:
            flash("No input provided")
            return render_template('/ngram_input.html')
        return redirect(url_for('ngram_post', in_text=in_text, nspan=nspan))
    return render_template('/ngram_input.html')

@app.route('/ngram_output', methods=['POST', 'GET'])
def ngram_post():
    nspan = int(request.args.get('nspan', '1'))
    text = request.args.get('in_text')
    ngrams = generate_ngrams(text, nspan)
    num_of_ngrams = len(ngrams)
    ngrams_dict = {str(k): v for k, v in ngrams.items()}

    return render_template("ngram_output.html",  ngrams=ngrams, num_of_ngrams=num_of_ngrams, ngrams_dict= ngrams_dict)


@app.route('/word_cloud_input', methods=['POST', 'GET'])
def wc_input():
    if request.method == 'POST':
        stop_w = request.form['stop_w']
        colormap = request.form['colormap']
        in_text = request.form['in_text']
        case = request.form['case']
        if len(in_text) == 0:
            flash("No input provided")
            return render_template('/word_cloud_input.html')
        return redirect(url_for('wc_post', stop_w=stop_w, in_text=in_text, colormap=colormap, case=case))
    return render_template('/word_cloud_input.html')

@app.route('/word_cloud_output', methods=['POST', 'GET'])
def wc_post():
    text = request.args.get('in_text')
    stop_w = request.args.get('stop_w', 'n_use')
    case = request.args.get('case', 'c_ins')
    cmap = request.args.get('colormap', 'spring')
    wc_cloud = generate_wordcloud(text, stop_w, case, cmap)
    wc_image = b64encode(wc_cloud).decode('utf-8')
    return render_template("word_cloud_output.html", wc_image=wc_image, case=case)


if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.run(port=5000, use_reloader=True)
