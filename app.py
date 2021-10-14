from logging import debug
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars")

@app.route("/")
def index():
    myVariable = mongo.db.marsDict.find_one()
    return render_template("index.html", marsData=myVariable)

@app.route("/scrape")
def scrape():
    marsDict = mongo.db.marsDict
    marsData = scrape_mars.scrape()

    marsDict.insert_one(marsData)
    return redirect("/",code=302)

if __name__ == "__main__":
    app.run(debug=True)
