from flask import Flask, render_template, session, request, flash, send_file, redirect, send_from_directory
import os
import sys
sys.path.insert(1, 'include/')

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['UPLOAD_FOLDER'] = './reciepts'

from routes import *