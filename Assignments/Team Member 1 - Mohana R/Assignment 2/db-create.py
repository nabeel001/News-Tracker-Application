import sqlite3
db_locale = 'users.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
CREATE TABLE auth 
(uno INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
pass TEXT
)
""")

connie.commit()
connie.close()