# Trending-Youtube-Videos_Analysis and Category predictor

Bubble plots visualizations using D3 of trending youtube videos from different locations(US, CA). Use of Naive Bayes classifier model to predict what category a video belongs to based on the title. 

![model](images/predict.png)
![svg](images/svg.png)
## Heatmap of correlation matrix
![corr](images/heat_corr.png)
## Most common words in video titles
![cloud](images/world_cloud.png)
## Published time
![pub](images/pub_Day.png)

## Review the project outline

Python: pandas, pymongo, flask, Naive Bayes model("probabilistic classifier"), spark (work in progress): tokenizer, hashing
Javascript: D3: event handlers, svg's, tool tips
html & css: forms
Procedure followed:

1 : Data in csv format is obtained from: 
https://www.kaggle.com/datasnaek/youtube-new#USvideos.csv
https://www.kaggle.com/datasnaek/youtube-new#CAvideos.csv

2. Data is inspected and prepared using panda dataframes

3. Dataframes are converted to dictionaries and fed to mongoDB 

4. Create a flask app that accesses our data from mongodb and later passes this data to a javascript program upon request. 

Using Javascript: 

Receive data from our flask app and do some analysis by grouping videos by category and generating a summary of the categories such as:
- average likes 
- average comments
- average dislikes
- average views 

6. Create an svg and create a bubble plot that holds some info of the category summmaries. Data visualizations are available for CA and US Trending youtube videos.

7. Use the Naive Bayes model to predict the category a video belongs to given the Title of the video. 


## Technology Used
<img src="https://raw.githubusercontent.com/david880110/tech-logo/master/python%20logo.png" width="240" height="50"/>
<img src="https://leafletjs.com/docs/images/logo.png" width="200" height="50"/>
<img src="https://www.bloorresearch.com/wp-content/uploads/2013/03/MONGO-DB-logo-300x470--x.png" width="200" height="130"/>
<img src="https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png" width="200" height="80"/>
<img src="https://4.bp.blogspot.com/-s2EhTt57oeU/XHtQtO1QNLI/AAAAAAAANW8/KYkPQEZUyocSpA2RzqCcVt31imXPi63RACLcBGAs/s1600/Free%2BCourses%2Bto%2Blearn%2BJavaScript.jpg" width="200" height="110"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Plotly-logo-01-square.png/1200px-Plotly-logo-01-square.png" width="200" height="75"/>
<img src="https://f0.pngfuel.com/png/447/350/apache-spark-logo-machine-learning-cluster-analysis-software-framework-spark-png-clip-art.png" width="240" height="50"/>




