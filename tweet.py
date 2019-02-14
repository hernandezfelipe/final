# importing the module 
import tweepy 
from datetime import datetime

def post_picture(image_path):

	# personal details 
	consumer_key ="ctzOeHT2AAgdy0lBJCvyFV6bl"
	consumer_secret ="859k6wWLvkcgyFOVy7HPTpCtLClHimzHICnvTitFbhvi4WrrBs"
	access_token ="878744744767172608-iO56XxpuXMK5OL6EtoXHrABgQ9LVB7d"
	access_token_secret ="pkCCCTxvoMVpuyaZf6e9SQKO46d3L1ubWIYlgINen799f"

	# authentication of consumer key and secret 
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

	# authentication of access token and secret 
	auth.set_access_token(access_token, access_token_secret) 
	api = tweepy.API(auth)
	now = datetime.now() 

	tweet = "Olar ("+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+")" # toDo 
	#image_path ="path of the image" # toDo 

	# update the status 
	status = api.update_with_media(image_path, tweet)  
	api.update_status(status) 


