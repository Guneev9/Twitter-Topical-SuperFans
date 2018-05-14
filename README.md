# Twitter Influential Users

Social Influence can be described as the ability to have an effect on the thoughts or actions of others. Influential members in on-line communities are becoming the new media to market products and sway opinions.Directed links in social media could represent anything from intimate friendships to common interests, or even a passion for breaking news or celebrity gossip. Such links determine the flow of information and further indicate a users influence on others. The objective of this analysis is to detect the influence in a specific topic on Twitter. In more detail, from a collection of tweets matching a specified query, we want to detect the influential users. In order to address this objective, we first want to focus our search on the individuals who write in their personal accounts based on that trending topic, so we investigated which set of features can best lead us to the topic-specific influential users, and how these features can be expressed in a model to produce a top list of influential users.Based on these measures, we investigate the dynamics of user influence across topics.We make several interesting observations.We believe that these findings provide new insights for viral marketing and suggest that topological measures such as re-tweets reveals a lot about the influence of a user.

## What is Influence?

Influence is the ability to drive action.These users are also called opinion leaders, innovators, prestigious or authoritative actors. Occasionally, they have been associated with topical experts for specific domains.
The problem of measuring the influence of a user in a social network is a conceptual problem. There is no agreement on what is meant by an influential user.


### How you Gain Influence On Twitter?

1. Retweets:

These tell you something about how willing people are to amplify your messages and help them spread. A retweet essentially says ”this is something I want my network to see”.

2. @Screenname
These signal how much others want to talk to you or intentionally tag you, and also serves as an indicator for how willing you are to engage and tag others. Less replies signals less social interactions and more broadcast.

3. Follower Count
Usually, if a user on Twitter follows more amount of users than than those who follow them, it signals their desire to accumulate followers. A 50/50 ratio translates to some- one following back anyone who follows them, which includes spammers. Twitter users who follow significantly less than are followed indicate some selection process.

4. Tweet volume
This simply indicates how prolific a user is. Those with high volumes who retain high levels of engagement, list counts, re-tweets, and a healthy ratio are likely providing some type of value.

5. Favorites
Getting favoritism frequently does mean something, though because Twitter users leverage Favorites so differently, it’s nearly impossible to discern exactly what, other than you triggered a behavior (the action to Favorite) for some reason.

6. Good Connections
The most difficult to quantify and probably the most important indicator is the quality
 5
and relevance of who follows you on Twitter and who you follow back. Targeting the right audience and earning their attention (and Trust) is ultimately the best.


### Influence Flow Score Implementation

Since influence is typically contextual, we have explored the effectiveness of the score across different domains. Users in domains were identified using the methodology described below, and ranked by their scores within their respective domains.In the context of a given Twitter community or topic, a particular user’s Influence Flow Score indicates how influential that user is within that community or topic.

I have calculated influence score for four different communities or you can say topic based on their hashtags:
1)♯WrestleMania
2)♯TaxDay
3)♯Metoo

Not limited to a specific tweet, Influence Flow Scores capture overall information flow in particular Twitter communities. Within the Fusion community (signified by ♯ hashtag), a certain user’s Influence Flow Score is calculated by the product of that user’s number of followers and number of times they mentioned hashtag and the parent user in their most recent 100 tweets.

## Algorithm Used

Following is the algorithm used for each community(topic):

a)Extraction of at least 100 users for each parent tweet based on their tweet id who have re-tweeted their tweet
b)Now, for every existing re-tweet id’s, we have followed the below steps:

  i)First extract the screen name and follower count of this re-tweeter user using the api function
  ii)Extraction of mentions of this user base don above hashtag and his parent screen name 
  iii)Calculation of score by multiplying his follower count and his total mentions
  iv)storing the scores along with other information in csv file
  
c)After performing the above steps for each parent, we will get csv files containing their re-tweeters and their score for further analysis

### Handling the CSV files

Once we have collected the information for each parent user in a file. We have further pre-processed each file for fetching the top 10 influencers of each parent along with their score. We also retrieved top 10 parent influencers of the community by summing up their re-tweeter’s score.
At last we have saved these final files for further visualizations and development of our user interface for more clarity.


### Functions Used for Implementation of Algorithm

1)retweet users of parent tweet(tweet id,screen name):
This function returns a collection of the 100 most recent re-tweets of the Tweet specified by the parent user id.It uses api.re-tweets to get the original tweets.At last,it returns the user id of re-tweeted user and screen-name of the parent user.
     
2)tweet user all tweets(user,n):
it filter out the tweets of re-tweet user based on hashtag and return the filtered tweets.

3)tweet user mentions(user,screen name):
it extracts total number of direct mentions of retweeters and their total re-tweets.

4)tweet user score(users,screen name):
This is the main function which is using all of the above functions to calculate the score fro each parent.It further returns the dictionary containing score and other related information. These are the major function definitions which are being used to fetch scores. There are other functions for visualizations.

## User InterFace

Notebooks come alive when interactive widgets are used. Users can visualize and control changes in the data. Learning becomes an immersive, plus fun, experience. Users can easily see how changing inputs to a model impacts the results. In this project, we are showing a notebook with one of the simplest interactive control elements and how it can be integrated in a data modeling task to dynamically visualize the impact of model parameter changing. We are using IPythons widgets for the same. We have two options for installing ipywid- gets. Basically, if we use pip, we also have to enable the ipywidget extension in our notebook to render it next time you start the notebook. We can enable it within any virtual environ- ment we use, so that the extension does not impact any other environment.
We followed the same process of enabling the ipywidget extension in our notebook. The same can also be done with the help of conda.
