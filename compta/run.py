from flask import Flask, render_template
import sys
sys.path.insert(1, 'include/')
from sqlInit import init_db
from sqlFuncs import check_table

app = Flask(__name__)

conn = init_db()
check_table(conn, "compta")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add')
def add():
    print ("Trying to add some spendings")
    return render_template("index.html")

@app.route('/exportmonth')
def exportmonth():
    print ("Trying to export some spendings monthly")
    return render_template("index.html")

@app.route('/exportyear')
def exportyear():
    print ("Trying to export some spendings yearly")

    return render_template("index.html")

app.run(debug=True)