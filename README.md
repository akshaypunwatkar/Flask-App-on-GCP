# Wordcloud generator for Twitter user

This project is an implementation of a simple python flask application on Google Cloud Platform (GCP).
The application can be accessed on this link :  https://carbide-acre-266720.appspot.com

## Getting Started

The application uses Flask in python for interacting with HTML pages of an application. Using the twitter userId as input, the app makes a call to twitter using the tweepy library and request the users timeline (tweets posted by the user). The maximum number of tweets which can be retrieved is 3200. However, the number of tweets could be less. The received tweets are processed using tweet-preprocessor, which is a library to process tweets. Hashtags and User mentions are extracted from the tweets using regualr expression. The text from tweets, hashtags, and user metions are used to generate wordclouds. The wordcloud response is then sent over via flask on the html web page.

## Prerequisites

The only prerequisite for this projects are the **Twitter developer credentials**, which are required to initialise communication of this application with Twitter. 

## Description of required files

> main.py : The main python file with the application code.   
> requirements.txt : List of packages needs to be installed during app deployment.   
> app.yaml : Contains environment configuration.   
> templates : Directory containing HTML template for the landing (index.html) and the response (results.html) page.    
> Makefile : File containing shell commands to execute requirements.txt and other configurations.     
> Twitter_GCP.ipynb : Application implementation in a jupyter notebook. For reference only, not actually required for app.    


## Links to documentation

> Flask :  https://flask.palletsprojects.com/en/1.1.x/    
> Wordcloud :  https://pypi.org/project/wordcloud/    
> Tweepy : http://docs.tweepy.org/en/v3.5.0/api.html    
> Tweet-preprocessor : https://pypi.org/project/tweet-preprocessor/    
> Google App Engine : https://cloud.google.com/appengine/docs/flexible/python/quickstart

# Authors

Akshay Punwatkar

## Acknowledgments

The project was developed under the guidance of Professor Noha Gift (https://noahgift.com) at Duke University. 
