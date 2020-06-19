from flask import Flask, render_template, session, request, flash, send_file, redirect
from random import randrange
import pandas as pd
import sys
import os
sys.path.insert(1, 'include/')
from sqlInit import init_db
from sqlFuncs import check_table, insert_table, print_table
from userHdl import create_user

app = Flask(__name__)
app.secret_key = os.urandom(12)
conn = init_db()
check_table(conn)
create_user(conn, "Dynnasty", "bite", "3")
conn.close()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template("login.html")
    conn = init_db()
    comptadata = print_table(conn, "compta")
    print(comptadata)
    amount = 0
    for rows in comptadata:
        amount = amount + rows[3]
        print(rows[3])
    return render_template("index.html",comptadata=comptadata, amount=amount)

@app.route('/loguser', methods=['POST'])
def logUser(status=None):
    conn = init_db()
    rows = print_table(conn, "users")
    for row in rows:
        print("loguser: trying user" + row[1])
        if request.form['password'] == row[2] and request.form['username'] == row[1]:
            session['logged_in'] = True
            conn.close()
            return redirect("/")
    conn.close()
    return redirect("/")

@app.route('/add', methods = ['POST', 'GET'])
def add():
    if not session.get('logged_in'):
        return render_template("login.html")
    if request.method == 'POST':
        args = [request.form["name"], request.form["desc"], request.form["amount"], request.form["date"]]
        print(args)
    # insert_table(conn, "compta", args)
    print ("Trying to add some spendings")
    conn.close()
    return redirect("/")

@app.route('/exportmonth')
def exportmonth():
    if not session.get('logged_in'):
        return render_template("login.html")
    print ("Trying to export some spendings monthly")
    return render_template("index.html")

@app.route('/exportyear')
def exportyear():
    if not session.get('logged_in'):
        return render_template("login.html")

    print ("Trying to export some spendings yearly")
    conn = init_db()
    rows = print_table(conn, "compta")
    pd.DataFrame(rows).to_csv("./compta.csv", sep='\t', header=["Number", "Name", "Description", "Amount", "Date"])
    return (send_file("./compta.csv"))
    return render_template("index.html")

app.run(debug=True)