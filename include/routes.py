from flask import Flask, render_template, session, request, flash, send_file, redirect, send_from_directory
from random import randrange
import pandas as pd
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
sys.path.insert(1, 'include/')
from sqlInit import init_db
from sqlFuncs import check_table, insert_table, print_table, update_row, delete_row
from userHdl import create_user, delete_user, update_user
from datetime import datetime
from __main__ import app

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
        if rows[6] != "Pending":
            amount = amount + rows[3]
    return render_template("index.html", comptadata=reversed(comptadata), amount=round(amount, 2), privilege = session['privilege'])

@app.route('/loguser', methods=['POST'])
def logUser(status=None):
    conn = init_db()
    rows = print_table(conn, "users")
    for row in rows:
        print("I: Looking for " + request.form['username'] + " trying user = " + row[1])
        if check_password_hash(row[2], request.form['password']) and request.form['username'] == row[1]:
            session['logged_in'] = True
            session['username'] = row[1]
            session['privilege'] = row[3]
            conn.close()
            return redirect("/")
    conn.close()
    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/add', methods = ['POST', 'GET'])
def add():
    conn = init_db()
    if not session.get('logged_in'):
        return render_template("login.html")
    if request.method == 'POST':
        if request.form["type"] == "neg":
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                filename = str(datetime.now()) + filename
                filename = secure_filename(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                args = [request.form["name"], request.form["desc"], "-" + request.form["amount"], request.form["date"], os.path.join(app.config['UPLOAD_FOLDER'], filename)]
            else:
                args = [request.form["name"], request.form["desc"], "-" + request.form["amount"], request.form["date"]]
        else:
            args = [request.form["name"], request.form["desc"], request.form["amount"], request.form["date"]]
        print(args)
    insert_table(conn, "compta", args)
    print ("I: New database entry inserted: " + request.form["name"])
    conn.close()
    return redirect("/")

@app.route('/exportmonth', methods=['POST'])
def exportmonth():
    conn = init_db()
    if not session.get('logged_in'):
        return render_template("login.html")
    if request.method == "POST":
        data = print_table(conn, "compta")
        res = []
        month = request.form['month']
        for row in data:
            print(row[4].split('-')[1])
            print("compared to:")
            print(request.form['month'])
            if (row[4].split('-')[1] == request.form['month']):
                res.append(row)
                print("Row added!")
        if len(res) == 0:
            return redirect('/')
        pd.DataFrame(res).to_csv("./compta" + month + ".csv", sep='\t', header=["Number", "Name", "Description", "Amount", "Date", "InvoicePath", "Approbation"])
        print ("I: Exporting data by month")
        return send_file("./compta" + month + ".csv")
        redirect('/')
    return redirect('/')

@app.route('/exportyear')
def exportyear():
    if not session.get('logged_in'):
        return render_template("login.html")
    print ("Trying to export some spendings yearly")
    conn = init_db()
    rows = print_table(conn, "compta")
    pd.DataFrame(rows).to_csv("./compta.csv", sep='\t', header=["Number", "Name", "Description", "Amount", "Date", "InvoicePath", "Approbation"])
    return (send_file("./compta.csv"))
    return render_template("index.html")

@app.route('/panel')
def panel():
    if not session.get('logged_in'):
        return render_template("login.html")
    if session.get('privilege') < '3':
        print ("Error: Attempted connection to admin panel from unauthorized user: " + session['username'])
        return redirect('/')
    conn = init_db()
    rows = print_table(conn, "users")
    return render_template("panel.html", users=rows, editstate="False")

@app.route('/adduser', methods=['POST'])
def adduser():
    if not session.get('logged_in'):
        return render_template("login.html")
    conn = init_db()
    rows = print_table(conn, "users")
    if request.method == 'POST':
        create_user(conn, request.form["username"], generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8), request.form["privilege"])
    return redirect('/panel')

@app.route('/deluser', methods=['POST'])
def deluser():
    if not session.get('logged_in'):
        return render_template("login.html")
    conn = init_db()
    if request.method == 'POST':
        delete_user(conn, request.form['username'])
    return redirect('/panel')

@app.route('/edituser', methods=['POST'])
def edituser():
    if not session.get('logged_in'):
        return render_template("login.html")
    conn = init_db()
    rows = print_table(conn, "users")
    if request.method == 'POST':
        username = request.form['name']
        for row in rows:
            if username == row[1]:
                args = [generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8), request.form['privilege']]
                print(request.form['password'])
                update_row(conn, "users", username, args)
                return redirect('/panel')
    return redirect('/panel')

@app.route('/reciepts/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/apprspend', methods=['POST'])
def approve():
    conn = init_db()
    if request.method == 'POST':
        name = request.form['id']
        rows = print_table(conn, "compta")
        for row in rows:
            if str(row[0]) == str(name):
                args = [row[2], str(row[3]), row[4], row[5], "Approved",row[1]]
                update_row(conn, "compta", name, args);
    return redirect('/')

@app.route('/delspend', methods=['POST'])
def delspend():
    conn = init_db()
    if request.method == 'POST':
        name = request.form['id']
        rows = print_table(conn, "compta")
        for row in rows:
            if str(row[0]) == str(name):
                delete_row(conn, "compta", name);
                print("Deleted row" + row[1])
    return redirect('/')

app.run(debug=True)

