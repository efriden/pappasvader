#powered by newsapi.org
import requests

def getTopNews():
	url = ('https://newsapi.org/v2/top-headlines?'
		   'country=se&'
		   'apiKey=6a17c0ed413c46efb97152947735a0d7')
	response = requests.get(url).json()

	l = []
	for i in response['articles']:
		l.append(i['title'])

	return l