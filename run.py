import db, os, json, requests, urllib, calendar, time
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from datetime import datetime
import csv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coins.json"
sep = ";"

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
	sql = "SELECT text FROM [coins_twitter.movie_actor_director] WHERE LOWER(text) LIKE \'%"
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

	if "rows" in query_response:
		return query_response["rows"]
	else:
		return []

# find all nominees
with open("results5.csv", "rb") as csvfile:

	csvfilereader = csv.reader(csvfile, delimiter=';')
	for row in csvfilereader:
				
		# prepare movie for twitter quers
		twit_movie = row[1].split(" - ")[0].split(":")[0].replace("The ", "")
		big_query_results = runBigQuery(twit_movie, datetime(2015, 1, 15), datetime(2015, 2, 22))

		for r in big_query_results:
			print row[2] + ';' + '"' + r["f"][0]["v"].replace("\n", "").replace("\r", "") + '"'

#with open("results5_positivity.csv", "wb") as f:
#    writer = csv.writer(f)
#    writer.writerows(results)
