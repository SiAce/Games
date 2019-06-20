import urllib.request, urllib.parse, urllib.error
import lxml.html, lxml.etree
import ssl
import re

with open('appid_list.txt', 'r') as appid_file:
    appid_str = appid_file.read()

appid_list = appid_str.split(',')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

app_prefix = "https://store.steampowered.com/app/"

appid = appid_list[0]

# Compose URL
app_url = app_prefix + appid

# Get HTML from Steam Web
response = urllib.request.urlopen(app_url, context=ctx)
html_str = response.read().decode()

# Save HTML file to local (Because parsing directly from web didn't work!)
with open("app.html", "w", encoding="utf-8" ) as html_file:
    html_file.write(html_str)

# Use lxml and XPath to find the name, reviews, date, genre
html = lxml.html.parse("app.html")
name_xpath = '/html/body/div[1]/div[7]/div[4]/div[1]/div[2]/div[2]/div[2]/div/div[3]/text()'
reviews_xpath = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[1]/div[2]/span[3]/text()'
#reviews_xpath = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[3]/text()'
release_date_xpath = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/text()'
#release_date_xpath = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[3]/div[2]/text()'

genre_xpath = '//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a[1]/text()'

name = html.xpath(name_xpath)
reviews = html.xpath(reviews_xpath)
release_date = html.xpath(release_date_xpath)
genre = html.xpath(genre_xpath)

name_str = str(name[0])
reviews_str = str(reviews[0])
release_date_str = str(release_date[0])
genre_str = str(genre[0])

print(name_str)
print(reviews_str)
print(release_date_str)
print(genre_str)

""" for appid in appid_list:

    # Compose URL
    app_url = app_prefix + appid

    # Get HTML from Steam Web
    response = urllib.request.urlopen(app_url, context=ctx)
    html_str = response.read().decode()

    # Save HTML file to local (Because parsing directly from web didn't work!)
    with open("app.html", "w", encoding="utf-8" ) as html_file:
        html_file.write(html_str)
    
    # Use lxml and XPath to find the script element which contains wishlist
    html = lxml.html.parse("app.html")
    name_xpath = '/html/body/div[1]/div[7]/div[4]/div[1]/div[2]/div[2]/div[2]/div/div[3]/text()'
    reviews_xpath = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[1]/div[2]/span[3]/text()'
    release_date_xpath = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/text()'
    genre_xpath = '//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a[1]/text()'

    name = html.xpath(name_xpath)
    reviews = html.xpath(reviews_xpath)
    release_date = html.xpath(release_date_xpath)
    genre_xpath = html.xpath(genre_xpath)

    script_str = str(nodes[0]) """
