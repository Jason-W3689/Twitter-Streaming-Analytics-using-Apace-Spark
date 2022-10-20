"""
    This Spark app connects to a script running on another (Docker) machine
    on port 9009 that provides a stream of raw tweets text. That stream is
    meant to be read and processed here, where top trending hashtags are
    identified. Both apps are designed to be run in Docker containers.

    To execute this in a Docker container, do:
    
        docker run -it -v $PWD:/app -p 5001:5001 --link twitter:twitter --name spark eecsyorku/eecs4415

    and inside the docker:

        spark-submit spark_app_sentiment.py

    For more instructions on how to run, refer to final tutorial 8 slides.

"""

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SQLContext
import sys
import requests

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
nltk.downloader.download('vader_lexicon')


# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter", 9009)

# Function to get pol_score


def get_pol_tupple(line):
    sia = SIA()
    result = []
    if ('#iOS' in line or '#Apple' in line):
        pol_score = sia.polarity_scores(line)
        if pol_score['compound'] < 0:
            result.append(('Apple_neg', 1))
        if pol_score['compound'] == 0:
            result.append(('Apple_neu', 1))
        if pol_score['compound'] > 0:
            result.append(('Apple_pos', 1))
    elif ('#Windows' in line or '#Microsoft' in line):
        pol_score = sia.polarity_scores(line)
        if pol_score['compound'] < 0:
            result.append(('Microsoft_neg', 1))
        if pol_score['compound'] == 0:
            result.append(('Microsoft_neu', 1))
        if pol_score['compound'] > 0:
            result.append(('Microsoft_pos', 1))
    elif ('#Android' in line or '#Google' in line):
        pol_score = sia.polarity_scores(line)
        if pol_score['compound'] < 0:
            result.append(('Google_neg', 1))
        if pol_score['compound'] == 0:
            result.append(('Google_neu', 1))
        if pol_score['compound'] > 0:
            result.append(('Google_pos', 1))
    elif ('#HarmonyOS' in line or '#HUAWEI' in line):
        pol_score = sia.polarity_scores(line)
        if pol_score['compound'] < 0:
            result.append(('HUAWEI_neg', 1))
        if pol_score['compound'] == 0:
            result.append(('HUAWEI_neu', 1))
        if pol_score['compound'] > 0:
            result.append(('HUAWEI_pos', 1))
    elif ('#IntelGaming' in line or '#Intel' in line):
        pol_score = sia.polarity_scores(line)
        if pol_score['compound'] < 0:
            result.append(('Intel_neg', 1))
        if pol_score['compound'] == 0:
            result.append(('Intel_neu', 1))
        if pol_score['compound'] > 0:
            result.append(('Intel_pos', 1))

    return result


pol_tupple = dataStream.flatMap(lambda line: get_pol_tupple(line))

# adding the count of each hashtag to its last count


def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)


# do the aggregation, note that now this is a sequence of RDDs
hashtag_pol_totals = pol_tupple.updateStateByKey(aggregate_tags_count)

# Func to send data to web
def send_kv_to_dashboard(kv):
    # extract the hashtags from dataframe and convert them into array
    top_tags = [item[0] for item in kv]
    # extract the counts from dataframe and convert them into array
    tags_count = [item[1] for item in kv]
    # initialize and send the data through REST API
    url = 'http://host.docker.internal:5001/updateData'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, data=request_data)

# process a single time interval


def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x: x[1], False)
        top10 = sorted_rdd.take(15)

        # Send data to webapp
        send_kv_to_dashboard(top10)

        # print it nicely
        for tag in top10:
            print('{:<40} {}'.format(tag[0], tag[1]))
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


# do this for every single interval
hashtag_pol_totals.foreachRDD(process_interval)


# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
