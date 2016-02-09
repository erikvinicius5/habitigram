from flask import Flask, url_for, request
import os
import requests

app = Flask(__name__)


def generate_telegram_method_url(method):
    return 'https://api.telegram.org/bot{token}/{method}'\
        .format(token=os.environ.get('TOKEN'), method=method)

@app.route("/")
def hello():
    return "Hello"

@app.route("/%s" % os.environ.get('ENCRYPTED_TOKEN'), methods=["POST"])
def post_update():
    print request.form

@app.route("/toggle_hook")
def toggle_hook():
    telegram_url = generate_telegram_method_url('setWebhook')
    certificate_path = '/static/certificates/public.pem'
    payload = { 'url': url_for(os.environ.get('ENCRYPTED_TOKEN')) }
    requests.post(telegram_url, data=payload, cert=certificate_path)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
