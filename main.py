from flask import Flask, render_template, request
import tweepy
import preprocessor as p
import re
import functools
import operator
from wordcloud import WordCloud
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def get_tweets():
    # initializing the twitter credentials

    consumer_key = "Your Consumer Key"
    consumer_secret = "Your Consumer Secret"
    access_key = "Your access key"
    access_secret = "Your access secret"

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    tweets = []

    if request.method == 'POST':
        user = request.form['userid']
        user = user.strip()

        # make initial request for most recent tweets
        new_tweets = api.user_timeline(screen_name=user, count=200)
        # save most recent tweets
        tweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = tweets[-1].id - 1
        while len(new_tweets) > 0:
            # print ("getting tweets before %s" % (oldest))
            new_tweets = api.user_timeline(screen_name=user,
                                           count=200, max_id=oldest)
            # save most recent tweets
            tweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = tweets[-1].id - 1
        # Extracting text body of the tweets from the tweets. 
        outtweets = [tweet.text for tweet in tweets]
        
        # Cleaning tweets and extracting hashtags and user mentions
        clean_tweets = [p.clean(tweet) for tweet in outtweets]
        hashtags_tweets = [re.findall(r'#(\w+)', tweet) for tweet in outtweets]
        mention_tweets = [re.findall(r'@(\w+)', tweet) for tweet in outtweets]
        all_hashtags = functools.reduce(operator.iconcat, hashtags_tweets, [])
        all_metion = functools.reduce(operator.iconcat, mention_tweets, [])

        # Initializing wordcloud object 
        wc = WordCloud(background_color="white", max_words=3000)
       
        text = ' '.join(clean_tweets)
        wc.generate(text)
        fig = Figure(figsize=[10, 10], dpi=120, edgecolor='black', frameon=False)

        # Generating wordcloud for the tweets 
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.imshow(wc, interpolation="bilinear")
        ax1.axis("off")
        ax1.set_title("\nWordcloud of recent tweets\n", fontsize=15)

        # Generating wordcloud for the hashtags
        hashtags_string = ' '.join(all_hashtags)
        wc.generate(hashtags_string)
        ax2 = fig.add_subplot(2, 2, 3)
        ax2.imshow(wc, interpolation="bilinear")
        ax2.axis("off")
        ax2.set_title("\nWord cloud of the Hashtags in the tweets\n", fontsize=10)

        # Generating wordcloud for the usermentions
        mention_string = ' '.join(all_metion)
        wc.generate(mention_string)
        ax3 = fig.add_subplot(2, 2, 4)
        ax3.imshow(wc, interpolation="bilinear")
        ax3.axis("off")
        ax3.set_title("\nWord cloud of the User mention in the tweets\n", fontsize=10)
        
        # Capturing the output plot and encoding it using Base64
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

        return render_template("results.html",
                               image=pngImageB64String, userId=user)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
