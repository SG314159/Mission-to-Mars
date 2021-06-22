# Module 10 exercises - Section 10.5.1
# Creating the Flask app for the Mission-to-Mars unit

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping   # scraping script from sections 10.3.3 to 10.3.5

app=Flask(__name__)

# Use flask_pymongo to setup mongo connection
# Tells Python that our app connects to Mongo using a URI (uniform resource indentifier)
app.config["MONGO_URI"]="mongodb://localhost.27017/mars_app"
# URI to connect our app to Mongo. Gives port and database name.
mongo=PyMongo(app)

# Route for the main html page. 
# The function links visual web app to the code that powers it.
@app.route("/")
def index():
    mars=mongo.db.mars.find_one() #find mars collection in db
    return render_template("index.html", mars=mars) #return template and use mars collection in MongoDB

# Route for scraping
@app.route("/scrape")
def scrape():
    mars=mongo.db.mars   # access the Mongo database
    mars_data=scraping.scrape_all()   #scrape new data using the script
    #update db; .update(query_parameter (empty JSON), data, options); upsert=create new docmt if one doesn't exist
    mars.update({}, mars_data, upsert=True)  
    return redirect('/',code=302)  #redirects user back to homepage; return message when successful

if __name__ == "__main__":
    app.run()


