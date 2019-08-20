import pymongo
import scrape_mars

client = pymongo.MongoClient()


def drop_all_collections(): 
    client.drop_database('web_scraping')
	
def write_mars_stories():
    contents = scrape_mars.download_nasa_mars_stories() 
    db = client['web_scraping']	
    for item in contents:
        db.mars_stories.insert_one(item)
		
def write_mars_space_facts():
    contents = scrape_mars.download_mars_space_facts()
    db = client['web_scraping']	
    for item in contents:   
        db.mars_space_facts.insert_one(item)
		
def write_weather_tweets():
    contents = scrape_mars.download_latest_mars_tweets()
    db = client['web_scraping']	
    for item in contents:   
        db.mars_weather_tweets.insert_one(item)

def write_hi_res_mars_images():
    contents = scrape_mars.download_hi_res_mars_images()
    db = client['web_scraping']
    for item in contents:
        db.mars_hi_res_mars_images.insert_one(item)

def get_mars_stories():
    results = []
    db = client['web_scraping']
    cursor = db.mars_stories.find({})
    for document in cursor:
	    results.append(document)
    return results
	
def get_weather_tweets():
    results = []
    db = client['web_scraping']
    cursor = db.mars_weather_tweets.find({})
    for document in cursor:
	    results.append(document)
    return results

def get_mars_space_facts():
    results = []
    db = client['web_scraping']
    cursor = db.mars_space_facts.find({})
    for document in cursor:
	    results.append(document)
    return results

def get_mars_hi_res_mars_images():
    results = []
    db = client['web_scraping']
    cursor = db.mars_hi_res_mars_images.find({})
    for document in cursor:
	    results.append(document)
    return results
#print (get_mars_stories())
#print(get_weather_tweets)
#print(get_mars_space_facts)
#print(get_mars_hi_res_mars_images)
#write_mars_space_facts()
#write_hi_res_mars_images()
#write_mars_stories()
#write_weather_tweets()