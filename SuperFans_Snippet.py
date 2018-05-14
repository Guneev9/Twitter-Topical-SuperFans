"""
This is the automated code snippet which is integrated with User Interface in order to perform the analysis dynamically
by simply givng any tranding hashtag.

It contains all. the required functions for:
1)Extraction of Tweets
2)Getting the retweet users of each parent
3)Calculation of influence score for each of this retweet user
4)Aggregation of scores to get scores of their parents
5)Storing the results in csv file
6)performing visualizaions on result characeristics

"""


#getting the necessary libraries
import tweepy
import json
import sys
import jsonpickle
import os
import time
import csv
import pandas as pd
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
from time import gmtime, strftime
from datetime import datetime
import time
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import bar
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import matplotlib.pyplot as plt
import warnings

#----------------------Function for connecting to twitter application----------------------

def authentication():  
    #Authentication 
    with open('auth_dict','r') as f:
        twtr_auth = json.load(f)

    # Replace the API_KEY and API_SECRET with your application's key and secret.
    #using app handler for faster results
    auth = tweepy.AppAuthHandler(twtr_auth['consumer_key'], twtr_auth['consumer_secret'])

    #API 
    api =tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    #checking connections
    if (not api):
        print ("Can't Authenticate")       
    
    return api

#----------------------Function for extracting the parent tweets based on given mention----------------------

def Tweets_Extraction(tweet,api=None):
    
    api=authentication()
    
    retries=0
    
    # this is the mention we ere looking for in twitter api
    Query =tweet 
    
    tweetCount =0
    # number of tweets to fetch
    maxTweets = 1000
    
    
    # We will store the tweets in a following json file in same directory.
    fName ='parent_Tweets_' + str(tweet[1:]) + '.json'

    all_tweets = []
    
    new_tweets = []
    with open(fName, 'w') as f:
        
        #For handling rate limits and other exceptions(retries)
        try:
        #used REST API for older tweets(one week older)
        #tweets for above query using cursor 
            data = tweepy.Cursor(api.search, q=Query,result_type = 'mixed').items(maxTweets)
         
        except tweepy.TweepError as e:
            print("Error when getting tweet: %s" % e)
            
        retries += 1
        
        if retries >= 100000:
            raise
        else:
            time.sleep(5)
        
        new_tweets = []
    
        #for checking the tweet data 
        for tweet in data:
            new_tweets.append(tweet)
        
        #saving tweets in a file
        for tweet in new_tweets:
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) +'\n')
        
        tweetCount += len(new_tweets)
        
    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

#----------------------Function for extracting retweeters for each parent user id ---------------------

#----base functions used in SuperFans function------------------
def retweet_users_of_parent_tweet(tweet_id,screen_name):
    
    #handling exceptions
    try:
        retweets = api.retweets(tweet_id, 100)
    
    #for removing the outliers
    except tweepy.TweepError as e:
        return None, e
    
    #returning id of retweeted user and screen-name of parent user 
    return [rt.user.id for rt in retweets],screen_name

def tweet_user_all_tweets(user,n,topic):
    
    #list of final tweets of a retweeted user
    result = []
    count = 0
    u_tweet=[]
        
    #including retweets and original tweets of this user(all tweets)    
    for tweet in tweepy.Cursor(api.user_timeline, id=user,include_rts=True).items(200):
        if re.findall(r"@%s" % topic, tweet._json['text'],re.I): 
            result.append(tweet._json)
    
    return result

def tweet_user_mentions(user,screen_name,topic):
    #first 2 pages tweets
    tweets = tweet_user_all_tweets(user, 2,topic)
    t_text = ''
        
    #extracting mentions here
    for t in tweets:
        t_text += t['text']
        
    # number of direct mentions + retweets
    return len(re.findall(r"@%s" % screen_name, t_text, re.IGNORECASE))

def tweet_user_score(users,screen_name,topic):
    
    #dictionary to store features
    user_dic = {}
    count = 0
    hashtag=topic
    for user in users:
        
        #getting the screen name of retweeted user
        retweeted_user_screen_name = api.get_user(id=user).screen_name
        
        #followers count of retweeted user
        follower = api.get_user(id=user).followers_count
                
        #getting mention of user
        mention = tweet_user_mentions(user,screen_name,topic)
        
        #score calculation
        user_dic[retweeted_user_screen_name] = [follower, mention, (follower*mention)]
        
        
        count += 1
        
        print (count, 'of', len(users), 'users added into dictionary')
        
        if count%20 == 0:
            print ('sleep for one minute')
            time.sleep(60)
            
    return user_dic


def Twitter_SuperFans(file,hashtag):
    retries=0
    count=0
    topic=hashtag
    for i in open(file,"r"):
        if i=="\n":
            next
        
        else:
            try:
            
                tweet = json.JSONDecoder().raw_decode(i)[0]
 
            except tweepy.TweepError as e:
                print("Error when getching the tweet: %s" % e)
            retries += 1
        
            if retries >= 10000:
                raise
            else:
                time.sleep(5)
    
        screen_name=tweet['user']['screen_name']
        tweet_id=tweet['id']
    
        retweet_id, par_screenname= retweet_users_of_parent_tweet(tweet_id,screen_name)
        
        #check if no user was found(Fake ids)
        if retweet_id is None:
            print ("Error in finding retweeter @{0}: {1}".format(screen_name, par_screenname))
            continue
    
        user_dic =tweet_user_score(retweet_id, par_screenname,topic)
    
        follower = [list(user_dic.values())[x][0] for x in range(len(user_dic))]
        mention = [list(user_dic.values())[x][1] for x in range(len(user_dic))]
        score = [list(user_dic.values())[x][2] for x in range(len(user_dic))]
    
        keys = []
        for i in user_dic.keys():
            keys.append(i)
        
        t_id = [tweet['id'] for x in range(len(user_dic))]
    
        newdic = {'tweet-id':tweet_id,'influencer':keys,'score':score,'mention':mention,'follower':follower,
                     'parent-user':screen_name,'retweet_id':retweet_id,}
    
        count += 1
    
        print ('-------',count,'Tweets Analyzed', '-------')
    
        df = pd.DataFrame(newdic)
    

        #storing the results in csv file
        df.to_csv(str(topic[1:]) + '_SuperFans' + '/' + screen_name  +  '.csv', encoding='utf-8')

#..................Function to pouplate top 10 influencers and top10 influencers of each user"

#Getting the csv's of SuperFans of WrestleMania
def Top10_influencers_of_parent(path,tweettag):
    
    home_dir=path
    SuperFans=[]

    #extract and sort files
    for _, _,files in os.walk(home_dir):
        for file in files:  
            SuperFans.append(file)
            SuperFans.sort(reverse=False)
        
    # Top 10 influencers of every parent user of WrestleMania
    Top_Influencers=pd.DataFrame()

    for f in SuperFans: #1000 
        #Open file
        parent_influencers=pd.read_csv(path + f, 'r',delimiter=',')
    
        if parent_influencers.empty:
            continue


        top10=parent_influencers.nlargest(10, 'score')
        top10.rename(columns={'follower': 'Follower', 'influencer': 'Influencer','mention':'User_Mentions',
                         'parent-user':'Parent_User','Retweet_id':'Retweet_ID','score':'Influence_Score',
                         'tweet_id':'Parent_user_id'}, inplace=True)
    
        Top_Influencers=top10.append(Top_Influencers)
        
    #storing the results in csv file
    Top_Influencers.to_csv('Top10_influencers_' + str(tweettag[1:]) + '.csv', encoding='utf-8')


def Top10_Influencers(path,tweettag):

    home_dir=path
    SuperFans=[]

    #extract and sort files
    for _, _,files in os.walk(home_dir):
        for file in files:  
            SuperFans.append(file)
            SuperFans.sort(reverse=False)
            
    Score=pd.DataFrame(columns=['User','Influence_Score'])

    score_index=-1

    for f in SuperFans: #1000 
        #Open file
        parent_influencers=pd.read_csv(path + f, 'r',delimiter=',')
    
        score_index +=1
    
        Score.set_value(score_index,'User',f[:-4])
    
        if parent_influencers.empty:
            Score.set_value(score_index,'Influence_Score', 0)
            continue
            
        else:
            total_score=parent_influencers['score'].sum()
            Score.set_value(score_index,'Influence_Score', total_score)
       
    Score.to_csv('Parent_influence_Score' + str(tweettag[1:]) + '.csv', encoding='utf-8')

#---------------------------------------------------------------------------------------
def twitter_cloud(tweettag):
    tweet=[]
    
    for i in open('parent_Tweets_' + str(tweettag[1:]) + '.json',"r"):
        if i=="\n":
            next
        else:
            #handling exceptions
            tweet.append(json.JSONDecoder().raw_decode(i)[0])

    warnings.filterwarnings('ignore')
    text=[]
    
    for i in tweet:
        text.append(i['text'])

    res = "".join(text)
    no_urls_no_tags = " ".join([word for word in res.split() if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'])


    mask = imread("./twitter_mask.png", flatten=True)

    wc = WordCloud(background_color="white", font_path="/Library/Fonts/Verdana.ttf", stopwords=STOPWORDS, width=7000,
                          height=800,mask=mask,colormap="Blues")
    wc.generate(no_urls_no_tags)
    plt.imshow(wc)
    plt.axis("off")

    plt.savefig('twitter_cloud.png', dpi=300)

#---------------------------------------------------------------
def graph_based_on_parent_user(Top_User,tweettag):
    
    df2= pd.read_csv('Top10_influencers_' + str(tweettag[1:]) + '.csv')
    df2=df2.drop(df2.columns[df2.columns.str.contains('unnamed',case = False)],axis = 1)
    #print(df2.head)
    #print(Top_User)
    d=df2.loc[df2['Parent_User']== Top_User]
    height = list(d['Influence_Score'])
    bars = list(d['Influencer'])
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height,width=0.8,color='blue',alpha=0.8)
    # Create names on the x-axis
    plt.xticks(y_pos, bars,rotation=90,color='black')
    plt.yticks(color='black')
    plt.xlabel('Top10 Twitter Users')
    plt.ylabel('Influence Scores')
    plt.grid(axis='y')
    #Show graphic
    print ("plotting Influence Scores of  " + Top_User)
    plt.show()

#-----------------------------------------------

def twitter_visualizations(tweettag):
    df1= pd.read_csv('Parent_influence_Score_' + str(tweettag[1:]) + '.csv')
    
    high_scorers=df1.nlargest(10, 'Influence_Score')
    high_scorers=high_scorers.drop(high_scorers.columns[high_scorers.columns.str.contains('unnamed',case = False)],axis = 1)
    Top_Users=list(high_scorers['User'])
    
    height = list(high_scorers['Influence_Score'])
    bars = list(high_scorers['User'])
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height,width=0.8,color='blue',alpha=0.8)
    # Create names on the x-axis
    plt.xticks(y_pos, bars,rotation=90,color='black')
    plt.yticks(color='black')
    plt.xlabel('Twitter Users')
    plt.ylabel('Influence Scores')
    plt.grid(axis='y')
    #Show graphic
    
    plt.show()
    
    return Top_Users

#---------------------------------API AUTHENTICATION---------------------------------   
api=authentication()

#-------------------------------------------------Sequence of function call----------------------------

"""
#Give hashtag here 
Trending_Topics= {1: '#HASHTAG'}

file_path=file_path='/SuperFans/'+ str(Trending_Topics[1][1:])

if not os.path.exists(str(Trending_Topics[1][1:] + '_SuperFans')):
    os.makedirs(str(Trending_Topics[1][1:]) + '_SuperFans')
          
home_path= str(Trending_Topics[1][1:]) + '_SuperFans'+ '/'

file='parent_Tweets_' + str(Trending_Topics[1][1:]) + '.json'

print("-------twitter authentication phase------------")
api=authentication()

#tweet means hashtag
print(".....................................tweets extraction phase................................")
Tweets_Extraction(Trending_Topics[1],api)

print(".....................................retweeters extraction phase................................")
Twitter_SuperFans(file,Trending_Topics[1])

print(".....................................Top 10 SuperFans of parent user's................................")
Top10_influencers_of_parent(home_path,Trending_Topics[1])

print(".....................................Top 10 SuperFans................................")
Top10_Influencers(home_path,Trending_Topics[1])
"""
