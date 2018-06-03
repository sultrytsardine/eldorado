from flask import Flask
from scraper import generatePhotoData

app = Flask(__name__)

@app.route('/generate-data/<user>', methods=['GET'])
def generateData(user):
    return generatePhotoData(user)