import aiohttp
import asyncio
import json






async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def main(itemHashes):
    header = {'X-API-Key': 'df73c07453de46fd89ec7b77312169a1'}

    vault = itemHashes
    itemURL = []
    items = []
    for i in vault:
        itemURL.append(
            'https://www.bungie.net/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(i[1]) + '/')
    print(itemURL)
    print(vault)
    urls = itemURL
    tasks = []
    async with aiohttp.ClientSession(headers=header) as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        for html in enumerate(htmls):
            if html[1]["Response"]["inventory"]["bucketTypeHash"] != 1469714392 and "plug" not in html[1]["Response"]:
                items.append([vault[0][0], html[1]["Response"]["displayProperties"]["name"],
                              html[1]["Response"]["inventory"]["tierTypeName"],
                              html[1]["Response"]["itemTypeDisplayName"],
                              'https://www.bungie.net' + html[1]["Response"]["displayProperties"]["icon"]
                              ])
        print(items)

def start(itemHashes):
    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(itemHashes))

