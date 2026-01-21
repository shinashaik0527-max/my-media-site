from flask import Flask, render_template, request, jsonify, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("media.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- HOME ----------
@app.route("/")
def home():
    media_type = request.args.get("type")
    conn = get_db_connection()

    if media_type:
        items = conn.execute(
            "SELECT * FROM media WHERE category = ? ORDER BY id DESC",
            (media_type,)
        ).fetchall()
    else:
        items = conn.execute(
            "SELECT * FROM media ORDER BY id DESC"
        ).fetchall()

    conn.close()
    return render_template("index.html", items=items)


# ---------- ADD (AJAX, NO REDIRECT) ----------
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        rating = request.form.get("rating")
        review = request.form.get("review")

        if not title or not category or not rating:
            return jsonify({"status": "error"}), 400

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO media (title, category, rating, review) VALUES (?, ?, ?, ?)",
            (title, category, rating, review)
        )
        conn.commit()
        conn.close()

        return jsonify({"status": "ok"})

    return render_template("add.html")


# ---------- SUGGEST ----------
@app.route("/suggest")
def suggest():
    conn = get_db_connection()
    item = conn.execute(
        "SELECT * FROM media WHERE rating >= 4 ORDER BY RANDOM() LIMIT 1"
    ).fetchone()
    conn.close()
    return render_template("suggest.html", item=item)


# ---------- DELETE ----------
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM media WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

