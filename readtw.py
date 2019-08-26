import tweepy
import pandas
import sys
import json
import smtplib, ssl
from email.mime.text import MIMEText

port = 465
password = input("Enter Password: ")
remail = input("Enter Target Email: ")

context = ssl.create_default_context()  

consumerKey = 'uuhqpIRLjONMMOVTgTuZwyiXf'
consumerSecret = 'jX2uOSv6TGTcEfQcPXXiHvIN5lH2DHW6QQkY83pex3PWApGp5x'
accessToken = '77843247-jBCaXCnViDluUaK1bAMA5IzEL0KLgKjMzwNHrJVNF'
accessTokenSecret = 'hxYNmmDiFpjQ3NvSKJnJAuEtGJYNNElIqfSRcUqBoDfrK'

auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#First, lets find the info for your Trends.

#ust = api.trends_place(2347572)
wort = api.trends_place(1)
#print(wort)
wort = wort[0]["trends"]

wtrends = []
i = 0
while i < 5: 
    wtrends.append(wort[i])
    i = i + 1 

#print(wtrends)

#print("Here are the most talked about things on Twitter, Worldwide:")

alltrends = ""
for trend in wtrends:
    alltrends = alltrends + trend["name"] + ": " + trend["url"] + "\n "

alltrends = alltrends.encode('ascii', 'ignore').decode('ascii')
#print("Here are the most talked about things in the United States:")
#Second, find the most interacted-with tweet on your timeline in the last day.

popstatus = []
allstatusi = api.home_timeline()
for i in range(0, 5):
    lar = 0
    lar_status = None
    for status in allstatusi:
        if status.favorite_count > lar and not status.retweeted:
            lar = status.favorite_count
            lar_status = status
            #print(lar_status)
            
    allstatusi.remove(lar_status)
    popstatus.append(lar_status)
        
#print("Conversations on your timeline to get involved in:")
allstatuses = ""
for status in popstatus:
    allstatuses = allstatuses + "https://twitter.com/user/status/" + status.id_str + "\n"

allstatuses = allstatuses.encode('ascii', 'ignore').decode('ascii')


#Third, Lets find news articles that might be important context for what you're going to need.


#Fourth, lets send an email with this information

etext =  """Here are the most talked about things on twitter, worldwide: \n""" + alltrends + """\nConversations on your timeline to get involved in:\n""" + allstatuses

mtext = MIMEText(etext)
mtext['From'] = "fordevjc@gmail.com"
mtext['To'] = remail
mtext['Subject'] = "Your Daily Twitter"


with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: 
    server.login("fordevjc@gmail.com", password)
    server.sendmail("fordevjc@gmail.com", remail, mtext.as_string())