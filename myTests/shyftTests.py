import json

vaultJson = open("myTests/vault.json", "r")
vault = json.load(vaultJson)

for a in vault:
    if len(a) > 11:
        print(a['itemHash'])