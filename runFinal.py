from pymongo import MongoClient
import db, os, json, requests, urllib, calendar, time
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coins.json"
sep = ";"
print "boxOfficeId" + sep + "twitter_mentions_after_nomination"

movie_cache = {}

# connect to mognodb
client = MongoClient(db.conn_string)
db = client.oscar

# grab the application's default credentials from the environment.
credentials = GoogleCredentials.get_application_default()

# construct the service object for interacting with the BigQuery API.
bigquery_service = build("bigquery", "v2", credentials=credentials)

# DATE TO UNIX
def dateToUnix(d):
	return float(calendar.timegm(time.strptime(str(d.day) + "/" + str(d.month) +  "/" + str(d.year), '%d/%m/%Y'))) * 1000.0

# RUN BIG QUERY
def runBigQuery(title):

	# build big query
	sql = "SELECT COUNT(*) FROM [twitter.twitter_2016] WHERE LOWER(content) LIKE \'%"
	sql += twit_movie.lower()
	sql += "%\' AND (LOWER(content) LIKE \'%"
	sql += "oscar"
	sql += "%\' OR LOWER(content) LIKE \'%"
	sql += "academy"
	sql += "%\')"
	sql += ";"

	# run query
	query_request = bigquery_service.jobs()
	query_data = {
		"query": (sql)
	}

	query_response = query_request.query(
	    projectId="coins-oscar",
	    body=query_data
	).execute()

	return query_response["rows"][0]["f"][0]["v"]

# find all nominees
for boxOfficeId in db.oscar_nominations.distinct("boxOfficeId"):


	boxId = boxOfficeId
	data = db.oscar_nominations.find_one({"boxOfficeId": boxId})
	boxOffice = db.boxoffice_movies.find_one({"boxOfficeId": boxId})

	if boxOffice.has_key("history"):
		releaseDate = boxOffice["history"][0]["date"]

	if not (boxId in movie_cache):
	
		# prepare movie for twitter quers
		twit_movie = data["film"].split(" - ")[0].split(":")[0].replace("The ", "")

		twitter_count = {}

		# if releaseDate:
		# 	twitter_count["before_release"] = runBigQuery(twit_movie, datetime(1970, 1, 1), releaseDate)
		# 	twitter_count["after_release"] = runBigQuery(twit_movie, releaseDate, datetime(data["year"] + 1, 2, 22))
		# else:
		# 	twitter_count["before_release"] = 0
		# 	twitter_count["after_release"] = 0

		twitter_count["after_nomination"] = runBigQuery(twit_movie)

	else:
		twitter_count = movie_cache[boxId]

	# [{u'f': [{u'v': u'51369'}]}]
	result = boxId + sep
	#result += twitter_count["before_release"] + sep
	#result += twitter_count["after_release"] + sep
	result += twitter_count["after_nomination"]

	# cache count
	if len(boxId) > 0:
		movie_cache[boxId] = twitter_count

	print result
