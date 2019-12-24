import urllib.request, urllib.parse, urllib.error
import lxml.html, lxml.etree
import ssl
import re
import csv

with open('appid_list.txt', 'r') as appid_file:
    appid_str = appid_file.read()

appid_list = appid_str.split(',')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

app_prefix = "https://store.steampowered.com/app/"

with open("data_steam.csv", "w", newline="") as data_steam_file:

    data_steam_writer = csv.writer(data_steam_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    data_steam_writer.writerow(["Names", "Reviews", "Release Date", "Genre"])

    for appid in appid_list:

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
        name_xpath_1 = '/html/body/div[1]/div[7]/div[4]/div[1]/div[2]/div[2]/div[2]/div/div[3]/text()'
        name_xpath_2 = '/html/body/div[1]/div[7]/div[4]/div[1]/div[2]/div[1]/div[2]/div/div[3]/text()'
        reviews_xpath_1 = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[1]/div[2]/span[3]/text()'
        reviews_xpath_2 = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[3]/text()'
        release_date_xpath_1 = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/text()'
        release_date_xpath_2 = '//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[3]/div[2]/text()'
        genre_xpath = '//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a[1]/text()'

        name_list_1 = html.xpath(name_xpath_1)
        name_list_2 = html.xpath(name_xpath_2)
        reviews_list_1 = html.xpath(reviews_xpath_1)
        reviews_list_2 = html.xpath(reviews_xpath_2)
        release_date_list_1 = html.xpath(release_date_xpath_1)
        release_date_list_2 = html.xpath(release_date_xpath_2)
        genre_list = html.xpath(genre_xpath)

        name_1 = str(name_list_1[0]).strip() if name_list_1 else ""
        name_2 = str(name_list_2[0]).strip() if name_list_2 else ""
        reviews_1 = str(reviews_list_1[0]).strip()[2:6].strip() if reviews_list_1 else ""
        reviews_2 = str(reviews_list_2[0]).strip()[2:6].strip() if reviews_list_2 else ""
        release_date_1 = str(release_date_list_1[0]).strip() if release_date_list_1 else ""
        release_date_2 = str(release_date_list_2[0]).strip() if release_date_list_2 else ""
        genre = str((genre_list)[0]).strip() if genre_list else "" 

        name = name_1 if name_1 else name_2
        reviews = reviews_2 if reviews_2 else reviews_1
        release_date = release_date_2 if release_date_2 else release_date_1
        genre = genre if genre else ""

        data_steam_writer.writerow([name, reviews, release_date, genre])
