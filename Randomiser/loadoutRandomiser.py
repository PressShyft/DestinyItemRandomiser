import grequests
import random
import json
import requests
from flask import Flask, render_template, session, abort, redirect, request, url_for



'''VARIABLES'''
global apiKey
global access_token
apiKey = 'df73c07453de46fd89ec7b77312169a1'
client_id = "35598"
client_secret = 'ptmCr9oGGAkp8a35JZcxzLDmX7Tn1vfXMOeCPlX.E2w'

itemHashes = []
itemURL = []
items = []
'''VARIABLES'''

AUTH_URL = f"https://www.bungie.net/en/OAuth/Authorize?client_id=" + client_id + "&response_type=code"
access_token_url = "https://www.bungie.net/platform/app/oauth/token/"

app = Flask(__name__)
app.config


@app.route("/")
@app.route('/index')
def index():
    code_created()
    return render_template('index.html', url=AUTH_URL)


def code_created():
    global code
    if 'code' in request.args:
        code = request.args.get('code')
        get_token(code)
    pass


def get_token(code):
    global access_token
    HEADERS = {'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': client_secret}
    response = requests.post(access_token_url, data=HEADERS, auth=(client_id, client_secret))

    tokens = json.loads(response.text)
    access_token = tokens['access_token']

    get_membership(access_token)


def get_membership(access_token):
    global apiKey
    url = "https://www.bungie.net/Platform/User/GetMembershipsForCurrentUser/"
    HEADERS = {'X-API-Key': apiKey, 'Authorization': 'Bearer ' + access_token}
    mem = requests.get(url, headers=HEADERS)
    membershipID = mem.json()['Response']['destinyMemberships'][0]['membershipId']
    get_hash(access_token, membershipID)
    #transfer(access_token)



def get_hash(access_token, membershipID):
    global apiKey
    testurl = f'https://www.bungie.net/Platform/Destiny2/3/Profile/{membershipID}/?components=102,302'
    HEADERS = {'X-API-Key': apiKey, 'Authorization': 'Bearer ' + access_token}
    res = requests.get(testurl, headers=HEADERS)
    vault = res.json()
    # print(vault)
    vaultHashes = vault["Response"]["profileInventory"]["data"]["items"]
    for a in vaultHashes:
        if len(a) > 11:
            tempDict = [a['itemInstanceId'], a["itemHash"]]
            # print(tempDict)
            itemHashes.append(tempDict)
    with open('vault.json', 'w') as f:
        json.dump(itemHashes, f, ensure_ascii=False, indent=4)
        vaultData(itemHashes)


def get_name(itemHashes):
    x = []
    for i in itemHashes:
        x.append('https://www.bungie.net/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(i[1]) + '/')
        HEADERS = {'X-API-Key': 'df73c07453de46fd89ec7b77312169a1'}
        res = requests.get(x, headers=HEADERS)
        names = res.json()
        print(names["Response"]["displayProperties"]["name"])


def vaultData(itemHashes):
    header = {'X-API-Key': 'df73c07453de46fd89ec7b77312169a1'}
    for i in itemHashes:
        itemURL.append(
            'https://www.bungie.net/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(i[1]) + '/')
    # print(itemURL)
    rs = (grequests.get(u, headers=header) for u in itemURL)
    html = grequests.map(rs)

    for i in enumerate(html):
        html[i[0]] = i[1].json()
        if html[i[0]]["Response"]["inventory"]["bucketTypeHash"] != 1469714392 and "plug" not in html[i[0]]["Response"]:
            items.append({
                "itemInstanceId": itemHashes[i[0]][0], 'itemID': itemHashes[i[0]][1], "name": html[i[0]]["Response"]["displayProperties"]["name"],
                "tierTypeName": html[i[0]]["Response"]["inventory"]["tierTypeName"],
                "itemTypeDisplayName": html[i[0]]["Response"]["itemTypeDisplayName"],
                "icon": 'https://www.bungie.net' + html[i[0]]["Response"]["displayProperties"]["icon"],
                "bucketTypeHash": html[i[0]]["Response"]["inventory"]["bucketTypeHash"]
            })
    #print(items)
    groupItems(items)


kineticWeapon = {'Legendary': [], 'Exotic': []}
energyWeapon = {'Legendary': [], 'Exotic': []}


def groupItems(items):
    for item in items:
        if item["bucketTypeHash"] == 1498876634:
            if item["tierTypeName"] == "Exotic":
                kineticWeapon['Exotic'].append(item)
            else:
                kineticWeapon['Legendary'].append(item)
        elif item["bucketTypeHash"] == 2465295065:
            if item["tierTypeName"] == "Exotic":
                energyWeapon['Exotic'].append(item)
            else:
                energyWeapon['Legendary'].append(item)
    # for i in kineticWeapon["Legendary"]: print(i['name'])
    randomWeapon(kineticWeapon, energyWeapon)

def randomWeapon(kineticWeapon, energyWeapon):
    exoticWpn = random.sample([0,1], 2)
    #randKinetic = random.choice(kineticWeapon[list(kineticWeapon)[exoticWpn[0]]])
    #randEnergy = random.choice(energyWeapon[list(energyWeapon)[exoticWpn[1]]])
    #print(randKinetic['name'])
    #print(randEnergy['name'])
    randWpn = [random.choice(kineticWeapon[list(kineticWeapon)[exoticWpn[0]]]), random.choice(energyWeapon[list(energyWeapon)[exoticWpn[1]]])]
    print(randWpn)
    transfer(access_token, randWpn)

def transfer(access_token, randWpn):
    url = f'https://www.bungie.net/Platform/Destiny2/Actions/Items/TransferItem/'
    HEADERS = {'X-API-Key': apiKey, 'Authorization': f'Bearer ' + access_token, "Content-Type": "application/json"}
    for wpn in randWpn:
        data = {"characterId":"2305843009877885004",
            "membershipType":3,
            "itemId": wpn['itemInstanceId'],
            "itemReferenceHash": wpn['itemID'],
            "stackSize":1,
            "transferToVault":False
        }
        payload = json.dumps(data)

        req = requests.post(url, data=payload, headers=HEADERS)
        res = req.json()
        print(res)
        print(req.status_code)




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



