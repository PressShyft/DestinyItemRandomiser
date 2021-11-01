import aiohttp
import asyncio
import json
import re

header = {'X-API-Key': 'df73c07453de46fd89ec7b77312169a1'}

vaultJson = open("../../Randomiser/vault.json", "r")
vault = json.load(vaultJson)
x = []
items = []
for i in vault:
    x.append('https://www.bungie.net/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(i) + '/')


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def main():
    urls = x
    tasks = []
    async with aiohttp.ClientSession(headers=header) as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            if "plug" in html["Response"]:
                print(html["Response"]["displayProperties"]["name"])
                items.append(
                    ['yo',html["Response"]["displayProperties"]["name"], html["Response"]["inventory"]["tierTypeName"],
                     html["Response"]["itemTypeDisplayName"],
                     re.findall('^(?:[^_]+_){2}([^_ ]+)', html["Response"]["plug"]["plugCategoryIdentifier"])])
            else:
                items.append(
                    [html["Response"]["displayProperties"]["name"], html["Response"]["inventory"]["tierTypeName"],
                     html["Response"]["itemTypeDisplayName"]])
        print(items)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
