from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
from flask import jsonify

# credential for hosting on Google Cloud Platform
credentials = GoogleCredentials.get_application_default()
ml = discovery.build('ml','v1', credentials=credentials)

projectID = 'projects/{}'.format('connoixer-183213/models/JenAesthetics_score')

def getPrediction(jsonFile):
	try:
		response = ml.projects().predict(name=projectID, body=jsonFile).execute()
		return response
	except errors.HttpError, err:
		return 'There was an error creating the model. Check the details:\n' + str(err._get_reason())

