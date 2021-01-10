import sqlite3
import requests
import json
import re
from lxml import etree
from io import StringIO, BytesIO



n_threads = 6
user_id = "276444078"



# Initialize SQLite Database
conn = sqlite3.connect('games.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Games (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Developer TEXT,
    Publisher TEXT,
    ScoreRank TEXT,
    Positive INTEGER,
    Negative INTEGER,
    Userscore INTEGER,
    Owners INTEGER,
    Average_forever INTEGER,
    Average_2weeks INTEGER,
    Median_forever INTEGER,
    Median_2weeks INTEGER,
    Price TEXT,
    Initialprice TEXT,
    Discount TEXT,
    Languages TEXT,
    Genre TEXT,
    ConcurrentUsers INTEGER
);
''')



# Compose URL
wishlist_prefix = "https://store.steampowered.com/wishlist/id/"

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
appid_list_new = re.findall('"appid":([0-9]+)', wishlist_str)

# Get old appid list from database
appid_list_old = [str(id_tuple[0]) for id_tuple in cur.execute('SELECT ID FROM Games')]

# Calculate the increment of the appid
appid_list_increment = list(set(appid_list_new) - set(appid_list_old))

print(appid_list_increment)

# Read webpages and write into database
app_prefix = "https://steamspy.com/api.php?request=appdetails&appid="

for appid in appid_list_increment:

    # Compose URL
    app_url = app_prefix + appid

    # Get HTML from Steam Web
    response = requests.get(app_url)
    html_str = response.text

    # Use json to parse json
    app_json = json.loads(html_str)

    entry = (
        app_json["appid"],
        app_json["name"],
        app_json["developer"],
        app_json["publisher"],
        app_json["score_rank"],
        app_json["positive"],
        app_json["negative"],
        app_json["userscore"],
        int(re.findall(r"(^\d+)\b", app_json["owners"].replace(",", ""))[0]),
        app_json["average_forever"],
        app_json["average_2weeks"],
        app_json["median_forever"],
        app_json["median_2weeks"],
        app_json["price"],
        app_json["initialprice"],
        app_json["discount"],
        app_json["languages"],
        app_json["genre"],
        app_json["ccu"]
    )

    cur.execute("INSERT INTO Games VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entry)

    conn.commit()

conn.close()

# Print success message
print(f'Done! {len(appid_list_increment)} entries inserted!')
