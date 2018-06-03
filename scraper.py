import urllib2
from bs4 import BeautifulSoup
import json
import re
import datetime
from flask import jsonify

def generatePhotoData(user):
    instagramUrl = 'https://www.instagram.com/{}/?hl=en'.format(user)
    images = openProfile(instagramUrl)
    return jsonify(extractPhotoData(images))

def openProfile(instagramUrl):
    page = urllib2.urlopen(instagramUrl)
    resultsJSON = extractPageJSON(page)

    return resultsJSON['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']

def getTimeTaken(unicodeTimestamp):
    return datetime.datetime.fromtimestamp(int(unicodeTimestamp)).strftime('%Y-%m-%d %H:%M:%S')

def setPhotoData(photoData):
    photo = {
        'caption': photoData['edge_media_preview_like']['count'],
        'likes': photoData['edge_media_to_caption']['edges'][0]['node']['text'],
        'time_taken': getTimeTaken(photoData['taken_at_timestamp'])
    }
    return photo

def extractPageJSON(page):
    # very brittle - need a better way to find the right script tag without relying on index
    scriptTagData = BeautifulSoup(page).find_all('script')[3].string
    windowSharedDataRegex = re.compile('window._sharedData = (.*?);')
    matchedData = windowSharedDataRegex.match(scriptTagData)
    return json.loads(matchedData.groups()[0])

def extractPhotoData(images):
    photos = []

    for i in range(0, len(images)):
        photo = urllib2.urlopen('https://www.instagram.com/p/{}/?hl=en&taken-by=tootins'.format(images[i]['node']['shortcode']))
        photoResultsJSON = extractPageJSON(photo)
        photoData = photoResultsJSON['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        photos.append(setPhotoData(photoData))

    return photos
