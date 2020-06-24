import findspark
from flask import Flask, render_template,json,jsonify
import requests
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
import pandas as pd


app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collections
db = client.trendingVideos

caTags = db.tagsCACollection




cat23 = (list(caTags.find({ 'category_id': 23 }))) 
tag23List = []
for i in cat23:
    tag23List.append(i["tags"].replace('|',' ').replace('"','').replace('/',' ').replace('#',''))
tag23Col = " ".join(tag23List)

cat24 = (list(caTags.find({ 'category_id': 24 })))
tag24List = []
for i in cat24:
    tag24List.append(i["tags"].replace('|',' ').replace('"','').replace('/',' ').replace('#',''))
tag24Col = " ".join(tag24List)

cat25 = (list(caTags.find({ 'category_id': 25 }))) 
tag25List = []
for i in cat25:
    tag25List.append(i["tags"].replace('|',' ').replace('"','').replace('/',' ').replace('#',''))
tag25Col = " ".join(tag25List)


newLista = []
newLista.append(tag23Col)
newLista.append(tag24Col)
newLista.append(tag25Col)


#print(newLista)
tagListDF = pd.DataFrame(newLista)
#print(type(tagListDF))
#print(tagListDF)


findspark.init()

from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StopWordsRemover
from pyspark.sql.types import StructField, StringType, IntegerType, StructType




# Start Spark session
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("tagTest").getOrCreate()



schema = [StructField("tags", StringType(), True)]
final = StructType(fields=schema)

dataframe2 = spark.createDataFrame((tagListDF))#,schema = final);

#dataframe2.show(truncate=False)

# Tokenize word
tokenizer = Tokenizer(inputCol="0", outputCol="tags")

tokenized = tokenizer.transform(dataframe2)
#tokenized.show(truncate=True)

#shall we remove stop words??
# remover = StopWordsRemover(inputCol="tags", outputCol="tagsRefined")
# remover.transform(tokenized).show(truncate=False)

hashing = HashingTF(inputCol="tags", outputCol="hashedValues", numFeatures=pow(2,5))
hashed_df = hashing.transform(tokenized)
hashed_df.show(truncate=False)















