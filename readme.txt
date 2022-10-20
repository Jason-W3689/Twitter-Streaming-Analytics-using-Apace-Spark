Note 1:
I cannot save the outputs to .txt files since I push them directly to the webapp
Please watch the demo video to see the background running status of the application.

Note 2:
The results are few because my computer is too weak to run either part for more than 20 minitues.
I had to captual the result before the computer overheats and reboots
With good computer the code would be able to produce all the desire outputs

Note 3:
Code can only run successfully in WSL. Modification is required in order to run this code on other operating systems

To run part1:

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




To run part2:

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