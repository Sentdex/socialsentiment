# Social Sentiment Dash Application
Live-streaming sentiment analysis application created with Python and Dash, hosted at [**SocialSentiment.net**](http://socialsentiment.net/).

![application example](https://github.com/Sentdex/socialsentiment/blob/master/DXzF9pyUQAAX1V7.jpg)

## Repo Contents: 
- `dash_mess.py` - This is currently the main front-end application code. Contains the dash application layouts, logic for graphs, interfaces with the database...etc. Name is descriptive of the overall state of code :) ...this code is setup to run on a flask instance. If you want to clone this and run it locally, you will be using the `dev_server.py`
- `dev_server.py` - If you wish to run this application locally, on the dev server, run via this instead.
- `twitter_stream.py` - This should run in the background of your application. This is what streams tweets from Twitter, storing them into the sqlite database, which is what the `dash_mess.py` file interfaces with. 
- `config.py` - Meant for many configurations, but right now it just contains stop words. Words we don't intend to ever count in the "trending"
- `cache.py` -  For caching purposes in effort to get things to run faster. 
- `db-truncate.py` - A script to truncate the infinitely-growing sqlite database. You will get about 3.5 millionish tweets per day, depending on how fast you can process. You can keep these, but, as the database grows, search times will dramatically suffer. 

## Quick start

- Clone repo
- install `requirements.txt` using `pip install -r requirements.txt`
- Fill in your Twitter App credentials to `twitter_stream.py`. Go to [**apps.twitter.com**](https://apps.twitter.com/) to set that up if you need to.
- Run `twitter_stream.py` to build database
- If you're using this locally, you can run the application with the `dev_server.py` script. If you want to deploy this to a webserver, see my [**deploying Dash application tutorial**](https://pythonprogramming.net/deploy-vps-dash-data-visualization/)
- Consider running the `db-truncate.py` from time to time (or via a cronjob), to keep the database reasonably sized. In its current state, the database really doesn't need to store more than 2-3 days of data most likely. 


## Todo

Want to help contribute???

- Code is ugly. Low hanging fruit is just making the code not so ugly. Up to this point, I've just been in "make it work" mode.
- App is ugly. I am not a designer. This app is prettttttyyyyyy gross. Think you have a better design? Halp. 
- Click-able related terms and trending terms would be nice. I tried, but failed at this. It'd be cool to see a related term, and be able to just click on it, and this becomes the new searched term, for example.
- The interactive search is cool, but also does a search in the database per-character. It would be nice if it didn't search per key-press. Not sure I want a search button, I like the streamlined interactivity, but maybe wait 0.2 seconds or something without any new keypresses to perform the search? Something like that might help with speeds. I really do not know the best option here, I just know this isn't idea.
- Other manipulations or ideas for interactivity? Feel free to show them in a PR.



