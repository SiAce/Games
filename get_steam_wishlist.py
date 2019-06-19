import urllib.request, urllib.parse, urllib.error
import lxml.html, lxml.etree
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Compose URL
steam_url = "https://store.steampowered.com/wishlist/profiles/"
user_id = input('Enter user id: ')
wishlist_url = steam_url + user_id

# Get HTML from Steam Web
response = urllib.request.urlopen(wishlist_url, context=ctx)
html_str = response.read().decode()

# Save HTML file to local (This is added because parsing directly from web didn't work!)
with open("wishlist.html", "w", encoding="utf-8" ) as html_file:
    html_file.write(html_str)

# Use lxml and XPath to find the wanted element
html = lxml.html.parse("wishlist.html")
xpathselector = "/html/body/div[1]/div[7]/div[4]/script/text()"
nodes = html.xpath(xpathselector)

print(nodes[0])