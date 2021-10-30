import urllib.parse
import json
import requests
from flask import Flask, render_template, session, abort, redirect, request, url_for


app = Flask(__name__)
app.config

client_id = "35598"
client_secret = 'ptmCr9oGGAkp8a35JZcxzLDmX7Tn1vfXMOeCPlX.E2w'

AUTH_URL = f"https://www.bungie.net/en/OAuth/Authorize?client_id=" + client_id + "&response_type=code"
access_token_url = "https://www.bungie.net/platform/app/oauth/token/"


@app.route("/")
@app.route('/index')
def index():
    code_created()
    return render_template('index.html', url=AUTH_URL)


def code_created():
    global code
    if 'code' in request.args:
        code = request.args.get('code')
        print('code:' + code)
        get_token(code)
    pass


def get_token(code):
    HEADERS = {'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': client_secret}
    response = requests.post(access_token_url, data=HEADERS, auth=(client_id, client_secret))

    tokens = json.loads(response.text)
    access_token = tokens['access_token']
    print(access_token)

    test_response(access_token)


def test_response(access_token):
    testurl = 'https://www.bungie.net/Platform/Destiny2/3/Profile/4611686018487036670/?components=102,302'
    HEADERS = {'X-API-Key': 'df73c07453de46fd89ec7b77312169a1', 'Authorization': 'Bearer ' + access_token}
    res = requests.get(testurl, headers=HEADERS)
    vault = res.json()
    print(vault)
    vaultHashes = vault["Response"]["profileIn0ventory"]["data"]["items"]
    print('yo')
    itemHashes = []
    for a in vaultHashes:
        if len(a) > 11:
            itemHashes.append(a['itemHash'])
    with open('vault.json', 'w') as f:
        json.dump(itemHashes, f, ensure_ascii=False, indent=4)






if __name__ == "__main__":
    app.secret_key = "password123abc"
    app.run(ssl_context='adhoc', port=80)
