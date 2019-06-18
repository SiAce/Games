import urllib.request, urllib.parse, urllib.error
import lxml
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

steam_url = "https://store.steampowered.com/wishlist/profiles/"
user_id = input('Enter user id: ')
wishlist_url = steam_url + user_id

response = urllib.request.urlopen(wishlist_url, context=ctx)
html = response.read().decode()

htmlparser = lxml.etree.HTMLParser()
tree = lxml.etree.parse(html, htmlparser)

xpathselector = "html/body/div[1]/div[7]/div[4]/script/text()"
data = tree.xpath("/html/body/div[1]/div[7]/div[4]/script")

print(data)