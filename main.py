import urllib2
from bs4 import BeautifulSoup
import json
import re
import datetime

photos = []
instagram = 'https://www.instagram.com/tootins/?hl=en'

def init():
    images = openProfile(instagram);
    extractPhotoData(images)

def openProfile(url):
    page = urllib2.urlopen(instagram)
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
    photos.append(photo)

def extractPageJSON(page):
    scriptTagData = BeautifulSoup(page).find_all('script')[2].string

    windowSharedDataRegex = re.compile('window._sharedData = (.*?);')
    matchedData = windowSharedDataRegex.match(scriptTagData)

    return json.loads(matchedData.groups()[0])

def extractPhotoData(images):
    for i in range(0, len(images)):
        photo = urllib2.urlopen('https://www.instagram.com/p/{}/?hl=en&taken-by=tootins'.format(images[i]['node']['shortcode']))
        photoResultsJSON = extractPageJSON(photo)
        photoData = photoResultsJSON['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        setPhotoData(photoData)


init()
print photos
