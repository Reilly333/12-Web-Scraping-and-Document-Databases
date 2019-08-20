import pandas
import requests
import progressbar
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'


def download_nasa_mars_stories(top_n_stories=50):
    """
    Downloads top N mars related sources from mars.nasa.gov
    :param top_n_stories: The number of stories you want to download (stored by time)
    :return: List of dictionaries (E.G [ {'title': 'Mars robot fucks unicorn', 'body': 'Scientists are baffled
        by a strange discovery on mars'}]
    """
    url = 'https://mars.nasa.gov/api/v1/news_items/?page=0&per_page={}' \
          '&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'.format(top_n_stories)
    resp = requests.get(url, headers={
        'user-agent': USER_AGENT, 'accept': 'application/json'
    })
    res = resp.json()
    items = res['items']
    stories = []
    for item in items:
        title, body = item['title'], item['body']
        soup = BeautifulSoup(body, features="html.parser")
        body = soup.getText().replace('\n', ' ').replace('\t', '')
        stories.append(
            {
                'title': title,
                'body': body
            }
        )
    return stories


def download_latest_mars_tweets(test=False, top=1):
    """
    Downloads mars related tweets from marswxreport (use test since this blatently goes against Twitter.com's EULA)
    :param test: True, if you want to pull from live twitter site, otherwise pulls test data from data/twitter-response.html
    :param top: The number of weather tweets you want to pull back
    :return: A list of top Mars weather tweets
    """
    weather_tweets = []

    def is_weather_tweet(tweet):
        """
        Basic test to determine if tweet is related to weather on mars
        :param tweet: Tweet text
        :return: True, if weather related tweet
        """
        if 'InSight' in tweet and 'sol' in tweet:
            return True
        return False

    url = 'https://twitter.com/marswxreport?lang=en'
    if not test:
        resp = requests.get(url, headers={'user-agent': USER_AGENT, 'accept': 'text/html'})
        response_data = resp.text
    else:
        response_data = open('data/twitter-response.html', 'r', encoding="utf-8").read()
    soup = BeautifulSoup(response_data, features="html.parser")
    tweets_html_p_tags = soup.find_all("p", class_="tweet-text")
    for tweet_html_p_tag in tweets_html_p_tags:
        tweet_text = tweet_html_p_tag.getText().replace('\n', ' ').replace('\t', '').replace('   ', '')
        if is_weather_tweet(tweet_text):
            weather_tweets.append({"tweet":tweet_text})
    return weather_tweets[0:top]


def download_mars_space_facts(as_html=True):
    """
    Goes to space-facts.com and grabs the table element from the page;
    Returning the exact same thing, but with a title (boy was that a round about way of accomplish this)

    :param as_html: If as_html returns the HTML table, otherwise returns a dictionary representation of the table
    :return: HTML representation of the table (with title) - or JSON if as_html=False
    """
    url = 'https://space-facts.com/mars/'
    resp = requests.get(url, headers=
        {'user-agent': USER_AGENT, 'accept': 'text/html'}
    )
    response_data = resp.text
    soup = BeautifulSoup(response_data, features="html.parser")
    mars_table_tag = soup.find("table", class_="tablepress-id-p-mars")
    mars_table_html = str(mars_table_tag)

    table_rows_df = pandas.read_html(mars_table_html)[0]
    table_rows_df.columns = ['Attribute', 'Value']
    table_rows_df.reset_index()
    if as_html:
        return table_rows_df.to_html()
    else:
        return table_rows_df.to_json()


def download_hi_res_mars_images():
    """
    Downloads a highres links and titles from https://astrogeology.usgs.gov
    :return: A list of dictionaries (E.G {'orginal_size_link': u'.../Viking/cerberus_enhanced.tif',
        'title': u'Cerberus Hemisphere Enhanced'}})
    """
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere%20enhanced&k1=target&v1=Mars'
    resp = requests.get(url, headers={
        'user-agent': USER_AGENT, 'accept': 'text/html'
    })
    response_data = resp.text
    soup = BeautifulSoup(response_data, features="html.parser")
    link_tags = soup.find_all('a', class_='product-item')
    hi_res_images = []
    for link_tag in progressbar.progressbar(link_tags):
        title = link_tag.find('h3').string
        base_url = 'https://astrogeology.usgs.gov/'
        new_url = base_url + link_tag['href']
        second_page_resp = requests.get(new_url, headers={'user-agent': USER_AGENT, 'accept': 'text/html'})
        second_page_response_data = second_page_resp.text
        soup = BeautifulSoup(second_page_response_data, features="html.parser")
        candidate_link_tags = soup.find_all('a')
        original_size_link = None
        for candidate_link_tag in candidate_link_tags:
            if candidate_link_tag.string == 'Original':
                original_size_link = candidate_link_tag['href']
                break
        hi_res_images.append(
            {
                'title': title,
                'orginal_size_link': original_size_link
            }
        )
    return hi_res_images