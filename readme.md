# Twitter Streaming Analytics using Apache Spark

## A. Twitter Trends Analysis

- This part of the program counts mentioning of any 5 '#Hashtags' in realtime and compare popularity among them.
- The program performs distributed compuation using **Apache Spark** engine.
- The result is visualized in real-time using **Flask**

## B. Real-time Sentiment Analysis of Twitter Topics

- This part of the program Collect tweets related to the 5 topics in real-time and perform sentiment analysis for each topic
- The sentimental analysis is performed using **NTLK**
- The result is visualized in real-time using **Flask**

## How to run the app

### To run 'A. Twitter Trends Analysis':

1. Fill in the credentials in twitter_app.py
2. Create two containers in Windows Subsystem of Linux (WSL) with Following command

	for twitter app: 
		docker run -it -v $PWD:/app --name twitter -p 9009:9009 python bash
		pip install tweepy
	for spark app:
		docker run -it -v $PWD:/app -p 5001:5001 --link twitter:twitter --name spark eecsyorku/eecs4415
	
3. Create a local WSL terminal
4. Run the twitter app in the first docker container with following command:
	python twitter_app.py
5. Run the webapp in HashtagsDashboard folder in local wsl termianl with following command:
	python3 app.py
6. Run the spark app in the second docker container with following command:
	spark-submit spark_app.py
7. Access localhost:5001 from the browser and you should be able to see the graph

### To run 'B. Real-time Sentiment Analysis of Twitter Topics':

1. Fill in the credentials in twitter_app.py
2. Create two containers in Windows Subsystem of Linux (WSL) with Following command

	for twitter app: 
		docker run -it -v $PWD:/app --name twitter -p 9009:9009 python bash
		pip install tweepy
	for spark app:
		docker run -it -v $PWD:/app -p 5001:5001 --link twitter:twitter --name spark eecsyorku/eecs4415
	
3. Create a local WSL terminal
4. Run the twitter app in the first docker container with following command:
	python twitter_app.py
5. Run the webapp in HashtagsDashboard_Sentiment folder in local wsl termianl with following command:
	python3 app.py
6. Run the spark app in the second docker container with following command:
	spark-submit spark_app_sentiment.py
7. Access localhost:5001 from the browser and you should be able to see the graph
