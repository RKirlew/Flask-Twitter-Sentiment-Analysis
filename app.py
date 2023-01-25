from flask import Flask
import tweepy
from tweepy import OAuthHandler
from flask import Flask, flash,render_template,request,redirect,url_for
import pymysql.cursors
import re
from textblob import TextBlob

app=Flask(__name__)
app.secret_key="flash message"
def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", str(tweet)).split()) 


@app.route("/")

def Index():
	
	return render_template('index.html')

@app.route("/search",methods=['POST','GET'])

def search():
	positive_ratio=0
	negative_ratio=0
	pTweets=[]
	nTweets=[]
	neTweets=[]
	neutral_ratio=0
	sakdk=0
	if request.method=="POST":
		consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
		consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		# set access token and secret
		auth.set_access_token(access_token, access_token_secret)
		# create tweepy API object to fetch tweets
		api = tweepy.API(auth)
		search=request.form['search']
		if '@'in search:
			users=api.get_user(screen_name=search)
		#user_img=users.profile_image_url
		fetched_tweets=api.search(q=search,count=100)
		for tweet in fetched_tweets:
			analysis=TextBlob(clean_tweet(tweet.text))
			if analysis.sentiment.polarity>0:
				positive_ratio+=1
				pTweets.append(tweet.text)
			elif analysis.sentiment.polarity==0:
				neutral_ratio+=1
				neTweets.append(tweet.text)
			else:
				negative_ratio+=1
				nTweets.append(tweet.text)
						
							
			
												
												
		return render_template('results.html',results=pTweets,pNum=positive_ratio,nNum=negative_ratio,iSearch=search,neNum=neutral_ratio,resultsN=nTweets,resultsNe=neTweets)
											
		

if __name__=="__main__":
	app.run(debug=True)
