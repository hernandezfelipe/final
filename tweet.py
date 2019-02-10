# importing the module 
import tweepy 
from datetime import datetime

def post_picture(image_path):

	# personal details 
	consumer_key ="j7xJJ6F8yuiQ18mlYNbxcqgAs"
	consumer_secret ="rmMcqZvhA6XoYuhPbgtJZecNVOTyt6w9OnwOspUQpJNDyMQWea"
	access_token ="878744744767172608-PPxpH99jPE5dRqqevrCnQZg2Uuk7WKZ"
	access_token_secret ="VLzEy8juokPnVRCdHUCgeHwwyU14YOgxQUZ7N2Zt5Ln8D"

	# authentication of consumer key and secret 
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

	# authentication of access token and secret 
	auth.set_access_token(access_token, access_token_secret) 
	api = tweepy.API(auth)
	now = datetime.now() 

	tweet = "Olar ("+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)+")" # toDo 
	#image_path ="path of the image" # toDo 

	# update the status 
	status = api.update_with_media(image_path, tweet)  
	api.update_status(status) 


