#################################################
# Import Dependencies
#################################################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Flask & PyMongo Setup
#################################################
# Create app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#################################################
# Flask Routes
#################################################
# Root route - Query Mongo DB and pass Mars data into HTML template
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

# Scrape route - Call scrape function from scrape_mars script
@app.route('/scrape')
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect('http://127.0.0.1:5000/')

if __name__ == '__main__':
    app.run(debug=True)