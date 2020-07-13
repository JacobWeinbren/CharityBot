#Work out the average number of likes and retweets + (likes/followers) + (retweets/followers)
import tweepy, logging

logger = logging.basicConfig()

auth = tweepy.OAuthHandler("fNUtHsbyjX2n3zNoBOLmFfpPA", "1v9Nfknvm0Q82Vps3xcoQgvFIkAMAJCDRDHsJmvpn9w9qJoEPr")
auth.set_access_token("987305245389803520-tt4CLdUli1v3T6tFs8pADfZhygcSJXY", "CU4G93o1hw97ry6sOdQWiHym8vpfQ071gw9jo42PcN8vi")

api = tweepy.API(auth)

charities = [
]

def getEngagement(charity):
    engagements = tweepy.Cursor(api.search, q=charity + " -from:" + charity, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items()
    count = 0

    for engagement in engagements:
        count += 1

    print(charity, count, 'engagement tweets')

#Thanks Malik
#https://stackoverflow.com/questions/31497631/tweepy-twitter-get-all-tweet-replies-of-particular-user
def countReplies(user_name, tweet_id):
    replies = tweepy.Cursor(api.search, q='to:'+user_name, since_id=tweet_id, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items()
    count = 0

    for reply in replies:
        if hasattr(reply, 'in_reply_to_status_id_str') and (reply.in_reply_to_status_id == tweet_id):
            count +=1

    return count

def getTweets(charity):
    retweets = []
    favourites = []
    replies = []
    count = 0
    search = tweepy.Cursor(api.search, q="from:" + charity, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items()

    for item in search:
        new_id = item.id
        replies.append(countReplies(charity, new_id))
        retweets.append(item.retweet_count)
        favourites.append(item.favorite_count)
        count += 1

    print(charity, "Tweets", count)

    if sum(retweets) > 0:
        print(charity, "Retweets Avg.", round(sum(retweets)/len(retweets)))
    else:
        print(charity, "Retweets Avg.", retweets)

    if sum(favourites) > 0:
        print(charity, "Favourites Avg.", round(sum(favourites)/len(favourites)))
    else:
        print(charity, "Favourites Avg.", favourites)

    if sum(replies) > 0:
        print(charity, "Replies Avg.", round(sum(replies)/len(replies)))
    else:
        print(charity, "Replies Avg.", replies)

for charity in charities:
    user = api.get_user(charity)
    print (charity, "Followers", user.followers_count)
    getEngagement(charity)
    getTweets(charity)