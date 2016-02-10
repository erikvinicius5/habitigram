from flask import Flask, url_for, request, Response
import os
import requests

app = Flask(__name__)


def generate_telegram_method_url(method):
    return 'https://api.telegram.org/bot{token}/{method}'\
        .format(token=os.environ.get('TOKEN', ''), method=method)

def get_full_url(url):
    return 'https://{server_name}{url}'\
        .format(server_name=os.environ.get('HEROKU_URL', ''), url=url_for(url))

@app.route("/")
def hello():
    return "Hello"

@app.route("/%s" % os.environ.get('ENCRYPTED_TOKEN', ''), methods=["POST"])
def post_update():
    print request.form['Message']
    return Response(json.dumps({ 'ok': True }), status=200)

@app.route("/toggle_hook")
def toggle_hook():
    value = request.args.get('value', '').lower() != 'false'
    telegram_url = generate_telegram_method_url('setWebhook')
    payload = { 'url': get_full_url('post_update') if value else '' }
    req = requests.post(telegram_url, data=payload)
    return req.text


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
