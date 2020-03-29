import sqlite3

conn = sqlite3.connect('games.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Games (
    ID int NOT NULL UNIQUE,
    Name varchar(255) NOT NULL,
    Developer varchar(255),
    Publisher varchar(255),
    ScoreRank varchar(255),
    Positive int,
    Negative int,
    Userscore int,
    Owners int,
    Average_forever int,
    Average_2weeks int,
    Median_forever int,
    Median_2weeks int,
    Price varchar(255),
    Initialprice varchar(255),
    Discount varchar(255),
    Languages varchar(255),
    Genre varchar(255),
    ConcurrentUsers int
);
''')


conn.commit()

conn.close()
