from tempfile import mkdtemp
import os
import random
from time import sleep

from flask import Flask, render_template, request

from functions import *

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

MEMES = []
d = "static/memes"
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isfile(full_path):
        MEMES.append(full_path)

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/entry", methods=["GET", "POST"])
def entry():
    """
    On GET, displays the page to enter partner hours and total ammount of tips

    On POST, requests partner names and respective hours, calculates the ammount of tips each partner is entitled to and total ammmount of each denomination needed to complete the job. 
    If the ammount cannot be rounded properly, the algorithm gives extra money, or subtracts missing money to make up the nearest $5.
    """
    if request.method == "GET":
        return render_template("entry.html", meme=random.choice(MEMES))
    else:
        partners = []
        hours = {}
        total_hours = float()
        print('hello')
        print(request.form.get("qty_partners"))
        for person in range(1, int(request.form.get("qty_partners")) + 1):
            name = request.form.get(f"name_{person}")
            if name:
                partners.append(name)
            else:
                partners.append(f"Person {person}")
        for person in partners:
            time = request.form.get(person)
            if time:
                hours[person] = time
                print(f'time type {type(time)}')
                total_hours += float(time)
        bank = int(request.form.get("bank"))
        payouts = {}
        total_rn = 0
        for partner in hours:
            if hours[partner]:
                payouts[partner] = round(float(hours[partner]) / total_hours * bank)
                total_rn += payouts[partner]
        if total_rn < bank:
            under = bank - total_rn
            while under > 0:
                monke = {}
                for partner in payouts:
                    sum = add_to_five(payouts[partner])
                    if sum > 0:
                        monke[partner] = sum
                print(monke)
                winner = min(monke, key=monke.get)
                payouts[winner] += monke[winner]
                under -= monke[winner]
        elif total_rn > bank:
            over = total_rn - bank
            while over > 0:
                monke = {}
                for partner in payouts:
                    sum = sub_to_five(payouts[partner])
                    if sum > 0:
                        monke[partner] = sum
                print(monke)
                winner = min(monke, key=monke.get)
                payouts[winner] -= monke[winner]
                over -= monke[winner]
        change = efficient_change(payouts)
        return render_template("results.html", payouts=payouts, notes=change)

if __name__ == "__main__":
    with app.app_context():
        app.run()
