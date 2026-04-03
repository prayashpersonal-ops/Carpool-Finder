from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("rides.db")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_ride", methods=["POST"])
def add_ride():
    data = request.json
    
    conn = get_db()
    conn.execute(
    "INSERT INTO rides (name, phone, start, destination, time, seats, cost, pin) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (data["name"], data["phone"], data["start"], data["destination"], data["time"], data["seats"], data["cost"], data["pin"])
)
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/get_rides")
def get_rides():
    conn = get_db()
    rides = conn.execute("SELECT * FROM rides").fetchall()
    conn.close()

    rides_list = []
    for r in rides:
        rides_list.append({
    "id": r[0],
    "name": r[1],
    "phone": r[2],
    "start": r[3],
    "destination": r[4],
    "time": r[5],
    "seats": r[6],
    "cost": r[7]
})
    

    return jsonify(rides_list)
@app.route("/delete_ride/<int:ride_id>", methods=["POST"])
def delete_ride(ride_id):
    data = request.json
    conn = get_db()

    ride = conn.execute(
        "SELECT pin FROM rides WHERE id = ?",
        (ride_id,)
    ).fetchone()

    if ride and str(ride[0]) == str(data["pin"]):
        conn.execute("DELETE FROM rides WHERE id = ?", (ride_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "deleted"})
    else:
        conn.close()
        return jsonify({"status": "wrong pin"})

if __name__ == "__main__":
    app.run(debug=True)