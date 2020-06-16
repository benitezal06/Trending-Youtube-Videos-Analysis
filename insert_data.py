import pandas as pd
import pymongo
import json

#DATA CLEAN UP 
 # Save path to data set in a variable
data_fileUS = "dataCSV/USvideos.csv"
data_fileCA = "dataCSV/CAvideos.csv"

 # Use Pandas to read data
data_file_pdUS = pd.read_csv(data_fileUS)
data_file_pdCA = pd.read_csv(data_fileCA)
##data_file_pd.head()

#eliminating unneccesary columns

usVideosDF = data_file_pdUS[["category_id","views","likes","dislikes","comment_count","title","video_id"]]
caVideosDF = data_file_pdCA[["category_id","views","likes","dislikes","comment_count","title","video_id"]]
# removing some for debug : "description","trending_date",
##usVideosDF

#checking for missing data 

##usVideosDF.count()

#NOTE: some records are missing description values

#category overview
##usVideosDF["category_id"].value_counts()
#NOTE: not all categories have trending videos

#views overview

views_summary = pd.DataFrame(usVideosDF["views"].describe())
views_min = usVideosDF["views"].min()
##print(views_min)
views_max = usVideosDF["views"].max()
##print(views_max)
views_mean = usVideosDF["views"].mean()
##print(views_mean)

#likes overview

likes_summary = pd.DataFrame(usVideosDF["likes"].describe())
likes_min = usVideosDF["likes"].min()
##print(likes_min)
likes_max = usVideosDF["likes"].max()
##print(likes_max)
likes_mean = usVideosDF["likes"].mean()
##print(likes_mean)

#comments overview

comments_summary = pd.DataFrame(usVideosDF["comment_count"].describe())
comments_min = usVideosDF["comment_count"].min()
##print(comments_min)
comments_max = usVideosDF["comment_count"].max()
##print(comments_max)
comments_mean = usVideosDF["comment_count"].mean()
##print(comments_mean)

#date manipulation
#dateSample = usVideosDF["trending_date"][0][0:2] +"/"+ usVideosDF["trending_date"][0][6:8]

#converting DataFrame into Dictionary

usVideosDict = usVideosDF.to_dict("records")
caVideosDict = caVideosDF.to_dict("records")
#print(usVideosDict)

#jsons that store category string, to be matched with numberical category from csv             
usCatJson = open("dataCSV/US_category_id.json",)
usCat = json.load(usCatJson)
#print(uScat)
caCatJson = open("dataCSV/CA_category_id.json",)
caCat = json.load(caCatJson)

#DATABASE

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.trendingVideos

db.usVideosCollection.drop()
db.usCatJsonCollection.drop()
db.caVideosCollection.drop()
db.caCatJsonCollection.drop()


usVideosCollection = db.usVideosCollection
usCatJsonCollection = db.usCatJsonCollection
caVideosCollection = db.caVideosCollection
caCatJsonCollection = db.caCatJsonCollection


usVideosCollection.insert_many(usVideosDict)
usCatJsonCollection.insert_one(usCat)
caVideosCollection.insert_many(caVideosDict)
caCatJsonCollection.insert_one(caCat)

print("Data Uploaded to Database!")
