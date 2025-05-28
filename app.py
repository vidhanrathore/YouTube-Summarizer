from flask import Flask, render_template, request, send_file
from utils.get_summary import summarize_article
from utils.get_yt_caption_using_url_or_id import get_captions
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    captions = ""
    url = ""

    if request.method == 'POST':
        url = request.form['youtube_url']
        max_len = int(request.form['summary_length'])
        captions = get_captions(url)
        summary = summarize_article(captions,use_cache=True,max_length=max_len)

    return render_template('index.html', summary=summary, captions=captions, url=url)

@app.route('/download', methods=['POST'])
def download():
    captions = request.form['captions']
    return send_file(
        io.BytesIO(captions.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name='captions.txt'
    )

if __name__ == '__main__':
    app.run(debug=True)
