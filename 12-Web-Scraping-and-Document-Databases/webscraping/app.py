# Flask app.py (controller) psuedocode

from flask import Flask
from flask import render_template, redirect, url_for, request, flash
import database



#localhost:5000/
app = Flask(__name__)

def get_home():
    return list_of_dict_to_html_table(database.get_weather_tweets()) + '<br><br>' + \
           list_of_dict_to_html_table(database.get_mars_stories()) + \
           '<br><br>' + database.get_space_facts()[0]['html']


@app.route("/mars_stories")
def mars_stories_page():
    mars_stories = database.get_mars_stories()
    if mars_stories is not None:
        return render_template('mars_stories.html', mars_stories=mars_stories)

@app.route("/weather_tweets")
def weather_tweets_page():
    weather_tweets = database.get_weather_tweets()
    if weather_tweets is not None:
        return render_template('weather_tweets.html', weather_tweets=weather_tweets)

@app.route("/mars_space_facts")
def mars_space_facts_page():
    mars_space_facts = database.get_mars_space_facts()[0]['html']
    if mars_space_facts is not None:
        return render_template('mars_space_facts.html', mars_space_facts=mars_space_facts)

@app.route("/mars_hi_res_mars_images")
def mars_hi_res_mars_images_page():
    mars_hi_res_mars_images = database.get_mars_hi_res_mars_images()
    if mars_hi_res_mars_images is not None:
        return render_template('mars_hi_res_mars_images.html', mars_hi_res_mars_images=mars_hi_res_mars_images)
		
@app.route("/")
def index_page():
    return render_template('index.html')
		
@app.route("/scrape")
def scraper():
    database.drop_all_collections()
    database.write_mars_space_facts()
    database.write_hi_res_mars_images()
    database.write_mars_stories()
    database.write_weather_tweets()
    return redirect('/')


if __name__ == "__main__":
    app.run()
