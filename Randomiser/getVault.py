import matplotlib.pyplot as plt
from PIL import Image
import io
import urllib.request

#image = Image.open('https://www.bungie.net/common/destiny2_content/icons/8c7681f1e93ee996a724e55554e079e9.jpg')

urllib.request.urlretrieve('https://www.bungie.net/common/destiny2_content/icons/8c7681f1e93ee996a724e55554e079e9.jpg', 'stmpees.jpg')

img = Image.open('stmpees.jpg')

img.show()

'https://www.bungie.net/common/destiny2_content/icons/8c7681f1e93ee996a724e55554e079e9.jpg'

''' FIND CLASS OF LEGENDARY ARMOUR (import re)
if 'plug' in item['Response']:
    print(re.findall('^(?:[^_]+_){2}([^_ ]+)', item["Response"]["plug"]["plugCategoryIdentifier"]))
'''