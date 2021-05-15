import requests

search_query = 'schubert'
number_of_results = 2
url = 'https://en.wikipedia.org/w/rest.php/v1/search/page'
headers = {'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'}

response = requests.get(url, headers=headers, params={'q': search_query, 'limit': number_of_results})
data = response.json()

print(data)