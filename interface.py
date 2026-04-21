from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from pymodbus.client import ModbusTcpClient
import webbrowser
webbrowser.open("http://127.0.0.1:5000")

app = Flask(__name__)
DB_FILE = "data.db"

# ---- Initialisation DB ----
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pannes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    travailleur TEXT,
                    panne TEXT,
                    technicien TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS techniciens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    telephone TEXT
                )''')
    conn.commit()
    conn.close()

# ---- Lecture Modbus ----
def lire_code_erreur():
    try:
        client = ModbusTcpClient("127.0.0.1", port=5020)
        client.connect()
        rr = client.read_holding_registers(0, 1, unit=1)
        client.close()
        if rr.isError():
            return "Erreur communication"
        return rr.registers[0]
    except:
        return "Non connecté"

# ---- API pour dernière panne ----
@app.route("/last_panne")
def last_panne():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT travailleur, panne, timestamp FROM pannes ORDER BY timestamp DESC LIMIT 1")
    last = c.fetchone()
    conn.close()
    if last:
        return jsonify({"travailleur": last[0], "panne": last[1], "timestamp": last[2]})
    return jsonify({})

# ---- Page principale ----
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        travailleur = request.form["travailleur"]
        panne = request.form["panne"]
        technicien = request.form["technicien"]

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO pannes (travailleur, panne, technicien) VALUES (?, ?, ?)",
                  (travailleur, panne, technicien))
        conn.commit()
        conn.close()
        return redirect("/")   #  important : toujours retourner

    # Sinon (GET), on affiche la page avec les données
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM techniciens")
    techniciens = c.fetchall()
    c.execute("SELECT * FROM pannes ORDER BY timestamp DESC")
    pannes = c.fetchall()
    conn.close()

    code_erreur = lire_code_erreur()

    return render_template("page.html",
                           techniciens=techniciens,
                           pannes=pannes,
                           code_erreur=code_erreur)

# ---- Lancement ----
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

