from flask import Flask, render_template, session, request, flash, send_file, redirect
from random import randrange
import pandas as pd
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
sys.path.insert(1, 'include/')
from sqlInit import init_db
from sqlFuncs import check_table, insert_table, print_table
from userHdl import create_user, delete_user, update_user

app = Flask(__name__)
app.secret_key = os.urandom(12)
conn = init_db()
check_table(conn)
conn.close()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template("login.html")
    conn = init_db()
    comptadata = print_table(conn, "compta")
    amount = 0
    for rows in reversed(comptadata):
        amount = amount + rows[3]
    return render_template("index.html",comptadata=reversed(comptadata), amount=amount)

@app.route('/loguser', methods=['POST'])
def logUser(status=None):
    conn = init_db()
    rows = print_table(conn, "users")
    for row in rows:
        print("loguser: trying user = " + row[1])
        if check_password_hash(row[2], request.form['password']) and request.form['username'] == row[1]:
            session['logged_in'] = True
            session['username'] = row[1]
            conn.close()
            return redirect("/")
    conn.close()
    return redirect("/")

@app.route('/add', methods = ['POST', 'GET'])
def add():
    conn = init_db()
    if not session.get('logged_in'):
        return render_template("login.html")
    if request.method == 'POST':
        print (request.form["type"])
        if request.form["type"] == "neg":
            args = [request.form["name"], request.form["desc"], "-" + request.form["amount"], request.form["date"]]
        else:
            args = [request.form["name"], request.form["desc"], request.form["amount"], request.form["date"]]
        print(args)
    insert_table(conn, "compta", args)
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

@app.route('/panel')
def panel():
    conn = init_db()
    rows = print_table(conn, "users")
    return render_template("panel.html", users=rows, editstate="False")

@app.route('/adduser', methods=['POST'])
def adduser():
    conn = init_db()
    rows = print_table(conn, "users")
    if request.method == 'POST':
        create_user(conn, request.form["username"], generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8), request.form["privilege"])
    return redirect('/panel')

@app.route('/deluser', methods=['POST'])
def deluser():
    conn = init_db()
    if request.method == 'POST':
        delete_user(conn, request.form['username'])
    return redirect('/panel')

@app.route('/edituser', methods=['POST'])
def edituser():
    conn = init_db()
    rows = print_table(conn, "users")
    if request.method == 'POST':
        delete_user(conn, request.form['username'])
    return render_template("panel.html", users=rows, editstate="")

app.run(debug=True)

