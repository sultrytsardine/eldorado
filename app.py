from flask import Flask
from scraper import load_photos

app = Flask(__name__)

@app.route('/photo-data/<user>', methods=['GET'])
def photo_data(user):
    return load_photos(user)

