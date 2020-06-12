from flask import Flask, render_template,json,jsonify
import requests
import pymongo
from bson import Binary, Code
from bson.json_util import dumps


app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collections
db = client.trendingVideos

usVideos = db.usVideosCollection
usCat = db.usCatJsonCollection

caVideos = db.caVideosCollection
caCat = db.caCatJsonCollection


trendingUS = list(usVideos.find())
usCatid = list(caCat.find())

trendingCA = list(caVideos.find())
caCatid = list(usCat.find())

@app.route("/",methods=['GET','POST'])
def index():

    return render_template("index.html",trendingUS = trendingUS)

@app.route("/us")
def us():
    
    return (dumps(trendingUS))

@app.route("/usid")
def usid():
    
    return (dumps(usCatid))

@app.route("/ca")
def ca():
    
    return (dumps(trendingCA))

@app.route("/caid")
def caid():
    
    return (dumps(caCatid))

if __name__ == "__main__":
    app.run(debug=True)



    