import urllib.request
import json

res = urllib.request.urlopen(
        "https://api.github.com/search/repositories?q=language:java&sort=stars&page=1&per_page=3&order=desc"
)
res = json.loads(res.read().decode('utf-8'))

for item in res['items']:
    print(item['full_name'])

