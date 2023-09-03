import sqlite3


db = sqlite3.connect('sqlKon.db')
cur = db.cursor()

# cur.execute('''CREATE TABLE zayv(
# id INTEGER PRIMARY KEY,
# zayvki text NOT NULL               
# )''')

cur.execute('''CREATE TABLE comm(
id INTEGER PRIMARY KEY,
comment text NOT NULL               
)''')
