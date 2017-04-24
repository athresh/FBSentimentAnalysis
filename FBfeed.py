import urllib.request
import json
import csv

app_id = "1863490403890772"
app_secret = "xgCLvFP3OE6eEULkiMJNL6_210E"

access_token = app_id + "|" + app_secret

page_id = 'nytimes'

def getFacebookPageData(page_id, access_token):
    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id + "/feed"
    parameters = "/?fields=message&access_token=%s" % access_token
    url = base + node + parameters

    # retrieve data
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    return data

FBdata = getFacebookPageData(page_id, access_token)
print(json.dumps(FBdata, indent=4, sort_keys=True))

#Format and write the feed to a csv file
count = 0
filepath = "C:/Users/Athresh/Documents/ATH ML/Python/FBfeedData.csv"

with open(filepath, 'a', newline='',encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    while count<len(FBdata['data']):
        writer.writerow([next(iter(FBdata['data'][count].values()))])
        count = count + 1




