from pymongo import MongoClient
import db, os, json, requests, urllib
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coins.json"
sep = ";"
print "year" + sep + "name"  + sep + "boxOfficeId" + sep + "won" + sep + "twitter_mentions"

# connect to mognodb
client = MongoClient(db.conn_string)
db = client.oscar

# grab the application's default credentials from the environment.
credentials = GoogleCredentials.get_application_default()

# construct the service object for interacting with the BigQuery API.
bigquery_service = build("bigquery", "v2", credentials=credentials)

# find all nominees
for data in db.oscar_nominations_extended.find():

	if data["film"]:

		# fetch boxOfficeId
		try:
			url_params = urllib.urlencode({"movie": data["film"], "year": str(data["year"])})
			resp = requests.get(url="http://boxofficeid.thomasbrueggemann.com/?" + url_params)
			boxData = json.loads(resp.text)

			boxId = boxData[0]["boxOfficeId"]
		except:
			boxId = ""

		try:

			# prepare movie for twitter quers
			twit_movie = data["film"].split(" - ")[0].split(":")[0].replace("The", "")

			# build big query
			sql = "SELECT COUNT(user.id_str) FROM [coins_twitter.movie_actor_director] WHERE LOWER(text) LIKE \'%"
			sql += twit_movie.lower()
			sql += "%\' AND (LOWER(text) LIKE \'%oscar%\' OR LOWER(text) LIKE \'%academy%\');"

			# run query
			query_request = bigquery_service.jobs()
			query_data = {
				"query": (sql)
			}

			query_response = query_request.query(
			    projectId="coins-1128",
			    body=query_data
			).execute()

			# [{u'f': [{u'v': u'51369'}]}]
			result = str(data["year"]) + sep
			result += data["film"] + sep
			result += boxId + sep

			if data["won"] == True:
				result += "1" + sep
			else:
				result += "0" + sep

			result += query_response["rows"][0]["f"][0]["v"]
			print result

		except:
			pass