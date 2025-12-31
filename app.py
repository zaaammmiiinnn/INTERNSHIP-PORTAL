from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    internships = conn.execute("SELECT * FROM internships").fetchall()
    conn.close()
    return render_template("index.html", internships=internships)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        location = request.form["location"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO internships (company, role, location) VALUES (?, ?, ?)",
            (company, role, location),
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM internships WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            location TEXT
        )
    """)
    conn.close()

    app.run(debug=True)
