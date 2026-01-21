import sqlite3

conn = sqlite3.connect("media.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    language TEXT,
    image_url TEXT,
    rating INTEGER NOT NULL,
    review TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully with images and series support.")
