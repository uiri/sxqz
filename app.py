import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    returnfile = open("home.tpl", 'r')
    returnstr = returnfile.read()
    return returnstr
