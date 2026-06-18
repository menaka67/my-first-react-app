from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("assignments.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            subject TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("assignments.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", assignments=data)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        subject = request.form["subject"]
        due_date = request.form["due_date"]

        conn = sqlite3.connect("assignments.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO assignments (title, subject, due_date) VALUES (?, ?, ?)",
            (title, subject, due_date)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add.html")

@app.route("/submit/<int:id>")
def submit(id):
    conn = sqlite3.connect("assignments.db")
    cur = conn.cursor()
    cur.execute("UPDATE assignments SET status='Submitted' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("assignments.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM assignments WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)