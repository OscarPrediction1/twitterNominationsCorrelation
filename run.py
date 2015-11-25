from pymongo import MongoClient
import db
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

# connect to mognodb
client = MongoClient(db.conn_string)
db = client.oscar

# grab the application's default credentials from the environment.
credentials = GoogleCredentials.get_application_default()

# construct the service object for interacting with the BigQuery API.
bigquery_service = build("bigquery", "v2", credentials=credentials)

try:
    # run query
    query_request = bigquery_service.jobs()
    query_data = {
        "query": (
            "SELECT TOP(corpus, 10) as title, "
            "COUNT(*) as unique_words "
            "FROM [publicdata:samples.shakespeare];")
    }

    query_response = query_request.query(
        projectId="coins-1128",
        body=query_data).execute()

    # print results
    print("Query Results:")
    for row in query_response["rows"]:
        print('\t'.join(field["v"] for field in row["f"]))

except HttpError as err:
    print('Error: {}'.format(err.content))
    raise err