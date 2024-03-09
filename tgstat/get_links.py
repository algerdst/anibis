import time

import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup


db = sqlite3.connect('tg_channels.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS tg_channels_info (
    name varchar(500),
    description text,
    subscribers varchar(50),
    img text,
    link varchar(500),
    category varchar(500)
)""")
db.commit()