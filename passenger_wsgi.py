import sys
import os

# Add project folder to path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
import main   # this imports your main.py

app = Flask(__name__)

@app.route("/")
def home():
    return "Scraper API Running"

@app.route("/run")
def run_script():
    main.main()   # make sure main.py has main() function
    return "Scraper executed successfully"

application = app
