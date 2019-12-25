import requests
import csv
import re
from lxml import etree
from io import StringIO, BytesIO

# Compose URL
wishlist_prefix = "https://store.steampowered.com/wishlist/id/"
user_id = "276444078"
wishlist_url = wishlist_prefix + user_id

# Get HTML from Steam Web
response = requests.get(wishlist_url)
html_str = response.text

# Set the parser
parser = etree.HTMLParser()
tree = etree.parse(StringIO(html_str), parser)

# Use lxml and XPath to find the script element which contains wishlist
wishlist_xpath = "/html/body/div[1]/div[7]/div[4]/script/text()"
nodes = tree.xpath(wishlist_xpath)
script_str = str(nodes[0])

# Use regular expression to extract the wishlist
wishlist_str = re.findall('var g_rgWishlistData = (\[.*\])', script_str)[0]
appid_list = re.findall('"appid":([0-9]+)', wishlist_str)

# Save the appid list
with open("appid_list.txt", "w") as appid_file:
    appid_file.write(','.join(appid_list))
