import time
import requests
import tkinter as tk
from tkinter import messagebox

FLASK_SERVER = "http://127.0.0.1:5000"

last_alert = None

def show_popup(travailleur, panne, timestamp):
    """Affiche un popup avec les infos d'alerte"""
    root = tk.Tk()
    root.withdraw()
    message = f"Travailleur: {travailleur}\nPanne: {panne}\nHeure: {timestamp}"
    messagebox.showinfo(" Nouvelle alerte de panne", message)
    root.destroy()

print("🔎 Agent de supervision démarré. En attente d'alertes...")

while True:
    try:
        r = requests.get(f"{FLASK_SERVER}/last_panne", timeout=5)
        if r.status_code == 200:
            data = r.json()

            if data:
                current_alert = (data.get("travailleur"), data.get("panne"), data.get("timestamp"))

                if current_alert != last_alert:
                    print(f"⚡ Nouvelle alerte : {current_alert}")
                    show_popup(*current_alert)
                    last_alert = current_alert
        else:
            print(f"Erreur HTTP {r.status_code} depuis Flask")

    except Exception as e:
        print(" erreur de connexion au serveur Flask:", e)

    time.sleep(5)

