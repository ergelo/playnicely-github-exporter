import settings

import urllib
import urllib2
import json

url = 'https://api.github.com/repos/ergelo/estetest/issues/79'

params = {"body": "implement reporting a false kill and deal with it in confirm_elimination", "title": "report false kill", "labels": [], "assignee": "ergelo", "milestone": "", "state": "Open"}

s = "%s:%s" % (settings.github_user, settings.github_password)

headers = { "Authorization": "Basic "+s.encode("base64").rstrip(), "Content-Type": "application/json" }

req = urllib2.Request(url, json.dumps(params), headers)

response = urllib2.urlopen(req)

print response.info()


