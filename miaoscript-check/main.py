import requests
import json
import time
from rich import print
from rich.pretty import pprint
import logging
from rich.logging import RichHandler
from rich.console import Console

from rich.traceback import install
install(show_locals=True)

console = Console(color_system='truecolor', width=65)

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("checker")

headers = {"content-type": "application/json"}

NPM_REGISTRY_ENDPOINT = 'https://registry.npmjs.org/'
SEARCH_REGISTRY_ENDPOINT = 'https://registry.koishi.chat/'

for _ in range(40):
	r = requests.get(SEARCH_REGISTRY_ENDPOINT)
	try:
		r.raise_for_status()
	except:
		logger.warn(r.text)
		
	result = r.json()
	plugins = result['objects']
	package_names = tuple(map(lambda p: p['shortname'], plugins))

	matches_pub = []
	matches_by_dep = []

	for idx, name in enumerate(package_names):
		if 'miao' in name or plugins[idx]['package']['publisher']['email'] == 'admin@yumc.pw':
			matches_pub.append(plugins[idx])
	
	for idx, name in enumerate(package_names):
		r1 = requests.get(f"{NPM_REGISTRY_ENDPOINT}{plugins[idx]['package']['name']}")
		try:
			r1.raise_for_status()
		except:
			continue
		package_info = r1.json()
		
		latest_version = package_info['dist-tags']['latest']

		latest_package_json = package_info['versions'][latest_version]
		latest_peer_deps = latest_package_json.get('peerDependencies', {})
		latest_deps = latest_package_json.get('dependencies', {})

		depend_with_peer_deps = any(match['package']['name'] in latest_peer_deps.keys() for match in matches_pub)

		depend_with_deps = any(match['package']['name'] in latest_deps.keys() for match in matches_pub)
		
		if depend_with_deps or depend_with_peer_deps:
			matches_by_dep.append(plugins[idx])

	print(
		*[f"{match['shortname']} | {match['package']['publisher']['username']} | {match['package']['version']}" for match in matches_pub]
		, sep='\n'
	)

	pprint(matches_pub)
	      
	logger.info("[green]complete", extra={"markup": True})
	
	time.sleep(90)
