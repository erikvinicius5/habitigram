from flask import Flask, url_for, request
import os
import requests

app = Flask(__name__)
app.config['SERVER_NAME'] = os.environ.get('HEROKU_URL', '')
app.config['PREFERRED_URL_SCHEME'] = 'https'


def generate_telegram_method_url(method):
    return 'https://api.telegram.org/bot{token}/{method}'\
        .format(token=os.environ.get('TOKEN', ''), method=method)

@app.route("/")
def hello():
    return "Hello"

@app.route("/%s" % os.environ.get('ENCRYPTED_TOKEN', ''), methods=["POST"])
def post_update():
    print request.form

@app.route("/toggle_hook")
def toggle_hook():
    telegram_url = generate_telegram_method_url('setWebhook')
    payload = { 'url': url_for('post_update') }
    req = requests.post(telegram_url, data=payload)
    return req.text


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
