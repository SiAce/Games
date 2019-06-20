import urllib.request, urllib.parse, urllib.error
import lxml.html, lxml.etree
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Compose URL
wishlist_prefix = "https://store.steampowered.com/wishlist/profiles/"
user_id = input('Enter user id: ')
wishlist_url = wishlist_prefix + user_id

# Get HTML from Steam Web
response = urllib.request.urlopen(wishlist_url, context=ctx)
html_str = response.read().decode()

# Save HTML file to local (Because parsing directly from web didn't work!)
with open("wishlist.html", "w", encoding="utf-8" ) as html_file:
    html_file.write(html_str)

# Use lxml and XPath to find the script element which contains wishlist
html = lxml.html.parse("wishlist.html")
wishlist_xpath = "/html/body/div[1]/div[7]/div[4]/script/text()"
nodes = html.xpath(wishlist_xpath)
script_str = str(nodes[0])

# Use regular expression to extract the wishlist
wishlist_str = re.findall('var g_rgWishlistData = (\[.*\])', script_str)[0]
appid_list = re.findall('"appid":([0-9]+)', wishlist_str)

# Save the appid list
with open("appid_list.txt", "w") as appid_file:
    appid_file.write(','.join(appid_list))
