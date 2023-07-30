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

for _ in range(40):
	r = requests.get("https://registry.koishi.chat")
	try:
		r.raise_for_status()
	except:
		logger.warn(r.text)
		
	result = r.json()
	plugins = result['objects']
	package_names = map(lambda p: p['shortname'], plugins)

	matches = []

	for idx, name in enumerate(package_names):
		if 'miao' in name or plugins[idx]['package']['publisher']['email'] == 'admin@yumc.pw':
			matches.append(plugins[idx])
	
	print(
		[f"{match['shortname']} {match['package']['publisher']['username']} {match['package']['version']}" for match in matches]
		, sep='\n')

	pprint(matches)
	      
	logger.info("[green]complete", extra={"markup": True})
	
	time.sleep(90)
