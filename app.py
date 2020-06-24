from flask import Flask, render_template,json,jsonify, request
import requests
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
import pandas as pd
#import collections
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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

@app.route("/")
def index():
    print("WE ARE IN: / ")

    
    return render_template("index.html",trendingUS = trendingUS)

@app.route('/predict',methods = ['POST', 'GET'])
def predict():
   print("we are in:/ predict")
   if request.method == 'POST':

    #load data
      USvids = pd.read_csv("dataCSV/USvideos.csv", header=0)
      USvids = USvids[['title','category_id']]
      Categories_JSON = pd.read_json("dataCSV/US_category_id.JSON")
    #create a dictionary
      CategoryDict = [{'id': item['id'], 'title': item['snippet']['title']} for item in Categories_JSON['items']]
      
    
      vector = CountVectorizer()
      counts = vector.fit_transform(USvids['title'].values)

      NB_Model = MultinomialNB()
      targets = USvids['category_id'].values

      #fit naive_bayes model with the titles and categories
      NB_Model.fit(counts,targets)

    #split the data
      X= counts
      y= targets
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .1)
    #train the model
      NBtest = MultinomialNB().fit(X_train, y_train)
    #test the model
      nb_predictions = NBtest.predict(X_test)
      acc_nb = NBtest.score(X_test, y_test)

      print('The Naive Bayes Algorithm scored an accuracy of', acc_nb)
      print("this is the form response:")
      #take a title from user input
      print(request.form["title"])
      titleList = []
      titleList.append(request.form["title"])
      print("this is the titleList")
      print(titleList)
      Titles_counts = vector.transform(titleList)

      #model makes prediction
      Predict = NB_Model.predict(Titles_counts)

    
      CategoryNamesList = []
      for Category_ID in Predict:
        MatchingCategories = [x for x in CategoryDict if x["id"] == str(Category_ID)]
        if MatchingCategories:
          CategoryNamesList.append(MatchingCategories[0]["title"])
    
        #obtain category prediction
        
   

      TitleDataFrame = []
      for i in range(0, len(titleList)):
        TitleToCategories = {'Title': titleList[i],  'Category': CategoryNamesList[i]}
        TitleDataFrame.append(TitleToCategories)
      #print(TitleToCategories)

      print(TitleToCategories['Category'])
      return render_template("index.html",pred = TitleToCategories['Category'])

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



    