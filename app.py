from flask import Flask, render_template, redirect
from flask_pymongo import pymongo

# From the separate python file in this directory, we'll import the code that is used to scrape mars
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# mongo = PyMongo(app)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# set database (used this first time to create db)
db=client.mars_db

# drop the data if already there so it doesn't append
db.mars_results.drop()

# db.mars_results.drop()

# Render the index.html page with any craigslist listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def home():
    return(f"Welcoming to Jeff's Scraping Application<br/><br/>"
        f"Please Visit /scrape to Begin Scraping<br/><br/>"
        f"After Scraping is Complete, You Will Be Returned to This Page")
    # listing_results = listings.find()
    # return render_template("index.html", listing_results=listing_results)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scraper():
    
    mars_data = scrape_mars.scrape()
    
    db.mars_results.insert_one(mars_data)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
