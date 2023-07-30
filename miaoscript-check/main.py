import json
import time
import logging
import asyncio

from aiohttp import ClientSession
from rich import print
from rich.pretty import pprint
from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

install(show_locals=True)

console = Console(color_system='truecolor', width=65)

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("checker")

headers = {"content-type": "application/json"}

NPM_REGISTRY_ENDPOINT = 'https://registry.npmjs.org/'
SEARCH_REGISTRY_ENDPOINT = 'https://registry.koishi.chat/'

async def scan_once():
	async with ClientSession(SEARCH_REGISTRY_ENDPOINT, headers=headers) as ss:
		async with ss.get(compress=True) as ss:	
			try:
				r.raise_for_status()
			except:
				logger.warn(r.text)
				raise
		
	result = r.json()
	plugins = result['objects']
	package_names = tuple(map(lambda p: p['shortname'], plugins))

	matches_pub = []
	matches_by_dep = []

	for idx, name in enumerate(package_names):
		if 'miao' in name or plugins[idx]['package']['publisher']['email'] == 'admin@yumc.pw':
			matches_pub.append(plugins[idx])
	
	async with ClientSession(NPM_REGISTRY_ENDPOINT, headers=headers) as session:
		for idx, name in enumerate(package_names):
			async with session.get(plugins[idx]['package']['name']) as r1:	
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
	
	return matches_pub, matches_by_dep

if __name__ == '__main__':

	loop = asyncio.create_loop()
	asyncio.set_event_loop(loop)

	for _ in range(0, 15):

		matches_pub, matches_by_dep = loop.run_util_complete(scan_once())

		print(
			*[f"{match['shortname']} | {match['package']['publisher']['username']} | {match['package']['version']}" for match in matches_pub]
			, sep='\n'
		)	

		logger.debug(matches_pub)
	      
		logger.info("[green]complete", extra={"markup": True})
	
		time.sleep(90)
