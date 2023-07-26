import requests
import json
import time

headers = {"content-type": "application/json"}

for _ in range(10):
	r = requests.get("https://registry.npmjs.org/koishi-plugin-miaoscript")
  	try:
  		r.raise_for_status()
	except:
  		print(r.text)

	result = r.json()
	try:
    		latest = result['dist-tags']['latest']
		assert latest=='0.0.1', f"Version mismatch {latest}"
	except Exception as e:
		print(e, r.text)

	print("complete ----------")

	time.sleep(60)
