from pymongo import MongoClient
import db, os, json, requests, urllib, calendar, time
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coins.json"
sep = ";"
print "year" + sep + "name"  + sep + "boxOfficeId" + sep + "won" + sep + "twitter_mentions_before_release" + sep + "twitter_mentions_after_release" + sep + "twitter_mentions_after_nomination"

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
def runBigQuery(title, startdate, enddate):

	# build big query
	sql = "SELECT COUNT(user.id_str) FROM [coins_twitter.movie_actor_director] WHERE LOWER(text) LIKE \'%"
	sql += twit_movie.lower()
	sql += "%\' AND (LOWER(text) LIKE \'%"
	sql += "oscar"
	sql += "%\' OR LOWER(text) LIKE \'%"
	sql += "academy"
	sql += "%\') AND timestamp_ms > "
	sql += "%f" % (dateToUnix(startdate))
	sql += " AND timestamp_ms < "
	sql += "%f" % (dateToUnix(enddate))
	sql += ";"

	# run query
	query_request = bigquery_service.jobs()
	query_data = {
		"query": (sql)
	}

	query_response = query_request.query(
	    projectId="coins-1128",
	    body=query_data
	).execute()

	return query_response["rows"][0]["f"][0]["v"]

# find all nominees
for data in db.oscar_nominations_extended.find():

	if data["film"] and data["year"] >= 2006:

		# fetch boxOfficeId
		try:
			url_params = urllib.urlencode({"movie": data["film"], "year": str(data["year"])})
			resp = requests.get(url="http://boxofficeid.thomasbrueggemann.com/?" + url_params)
			boxData = json.loads(resp.text)

			boxId = boxData[0]["boxOfficeId"]
			releaseDate = datetime.strptime(boxData[0]["release"], "%Y-%m-%dT%H:%M:%S.000Z")
		except:
			boxId = ""
			releaseDate = None

		if len(boxId) > 0:

			try:

				if not (boxId in movie_cache):
				
					# prepare movie for twitter quers
					twit_movie = data["film"].split(" - ")[0].split(":")[0].replace("The ", "")

					twitter_count = {}

					if releaseDate:
						twitter_count["before_release"] = runBigQuery(twit_movie, datetime(1970, 1, 1), releaseDate)
						twitter_count["after_release"] = runBigQuery(twit_movie, releaseDate, datetime(data["year"] + 1, 2, 22))
					else:
						twitter_count["before_release"] = 0
						twitter_count["after_release"] = 0

					twitter_count["after_nomination"] = runBigQuery(twit_movie, datetime(data["year"] + 1, 1, 15), datetime(data["year"] + 1, 2, 22))

				else:
					twitter_count = movie_cache[boxId]

				# [{u'f': [{u'v': u'51369'}]}]
				result = str(data["year"]) + sep
				result += data["film"] + sep
				result += boxId + sep

				if data["won"] == True:
					result += "1" + sep
				else:
					result += "0" + sep

				result += twitter_count["before_release"] + sep
				result += twitter_count["after_release"] + sep
				result += twitter_count["after_nomination"]

				# cache count
				if len(boxId) > 0:
					movie_cache[boxId] = twitter_count

				print result
			
			except:
				pass
