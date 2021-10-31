import urllib.parse
import json
import requests
from flask import Flask, render_template, session, abort, redirect, request, url_for
import GetWeaponData
global apiKey

app = Flask(__name__)
app.config

apiKey = 'df73c07453de46fd89ec7b77312169a1'
client_id = "35598"
client_secret = 'ptmCr9oGGAkp8a35JZcxzLDmX7Tn1vfXMOeCPlX.E2w'

AUTH_URL = f"https://www.bungie.net/en/OAuth/Authorize?client_id=" + client_id + "&response_type=code"
access_token_url = "https://www.bungie.net/platform/app/oauth/token/"

itemHashes = []


@app.route("/")
@app.route('/')
def index():
    code_created()
    print('1')
    return render_template('index.html', url=AUTH_URL)


def code_created():
    global code
    print('2')
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

    get_membership(access_token)


def get_membership(access_token):
    global apiKey
    url = "https://www.bungie.net/Platform/User/GetMembershipsForCurrentUser/"
    HEADERS = {'X-API-Key': apiKey, 'Authorization': 'Bearer ' + access_token}
    mem = requests.get(url, headers=HEADERS)
    membershipID = mem.json()['Response']['destinyMemberships'][0]['membershipId']
    print(membershipID)
    get_hash(access_token, membershipID)


def get_hash(access_token, membershipID):
    global apiKey
    testurl = f'https://www.bungie.net/Platform/Destiny2/3/Profile/{membershipID}/?components=102,302'
    HEADERS = {'X-API-Key': apiKey, 'Authorization': 'Bearer ' + access_token}
    res = requests.get(testurl, headers=HEADERS)
    vault = res.json()
    # print(vault)
    vaultHashes = vault["Response"]["profileInventory"]["data"]["items"]
    print('4')
    for a in vaultHashes:
        if len(a) > 11:
            tempDict = [a['itemInstanceId'],a["itemHash"]]
            print(tempDict)
            itemHashes.append(tempDict)
    with open('vault.json', 'w') as f:
        json.dump(itemHashes, f, ensure_ascii=False, indent=4)

        await GetWeaponData.start(itemHashes)


def get_name(itemHashes):
    for i in itemHashes:
        url = 'https://www.bungie.net/Platform/Destiny2/Manifest/DestinyInventoryItemasync definition/' + str(i[1]) + '/'
        HEADERS = {'X-API-Key': 'df73c07453de46fd89ec7b77312169a1'}
        res = requests.get(url, headers=HEADERS)
        names = res.json()
        print(names["Response"]["displayProperties"]["name"])



def get_item(access_token, membershipID):
    global apiKey
    HEADERS = {'X-API-Key': apiKey, 'Authorization': 'Bearer ' + access_token}
    vaultItemsJson = open("vault.json", "r")
    vaultItems = json.load(vaultItemsJson)
    weaponInfo = []
    print("wow")
    for a in vaultItems:

        url = f"https://www.bungie.net/Platform/Destiny2/3/Profile/{membershipID}/Item/{a}/?components=300,302,307"
        weaponSpecific = requests.get(url, headers=HEADERS)
        weapon = weaponSpecific.json()
        weaponInfo.append(weapon)
        print(weapon)
    print(weaponInfo)


if __name__ == "__main__":
    app.secret_key = "password123abc"
    app.run(ssl_context='adhoc', port=8080)
