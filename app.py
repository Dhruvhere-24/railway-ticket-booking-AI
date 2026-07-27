# app.py
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from db import get_connection
from Agent.agent import Start_agent

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ==================== HOME ====================
@app.route("/")
def home():return render_template("index.html")

def ai_respons(user_message):return Start_agent(user_message)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    message = data.get("message", "")
    response = ai_respons(message)

    return jsonify({
        "response": response
    })

# ==================== ADMIN LOGIN ====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        admin = cur.fetchone()
        cur.close()
        conn.close()

        if admin:
            session["admin"] = admin["username"]
            return redirect("/admin")
        else:
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

# ==================== ADMIN PANEL ====================
@app.route("/admin")
def admin_panel():
    if "admin" not in session:
        return redirect("/login")
    return render_template("admin_panel.html")

@app.route("/admin/add_train", methods=["GET", "POST"])
def add_train():
    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        number = request.form["number"]
        name = request.form["name"]
        dep = request.form["departure"]
        arr = request.form["arrival"]
        days = request.form["days"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO trains (number, name, departure_time, arrival_time, days)
            VALUES (%s, %s, %s, %s, %s)
        """, (number, name, dep, arr, days))
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/timetable")

    return render_template("add_train.html")

# ==================== BOOKING ====================
@app.route("/book", methods=["GET", "POST"])
def book_ticket():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM trains")
    trains = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        train_id = request.form["train_id"]
        # date = request.form["date"]
        date = request.form.get("date")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO bookings (name, age, gender, train_id, travel_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, gender, train_id, date))
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/bookings")

    return render_template("book_ticket.html", trains=trains)

@app.route("/bookings")
def view_bookings():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.id, b.name, b.age, b.gender, b.travel_date,
               t.name AS train_name, t.number
        FROM bookings b
        JOIN trains t ON b.train_id = t.id
    """)
    bookings = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("view_bookings.html", bookings=bookings)

# ==================== CANCEL BOOKING ====================
@app.route("/cancel", methods=["GET", "POST"])
def cancel_ticket():
    if request.method == "POST":
        booking_id = request.form["booking_id"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/bookings")

    return render_template("cancel_ticket.html")

# ==================== TIMETABLE ====================
@app.route("/timetable")
def timetable():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM trains")
    trains = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("timetable.html", trains=trains)

# ==================== MAIN ====================
if __name__ == "__main__":
    app.run(debug=True)
