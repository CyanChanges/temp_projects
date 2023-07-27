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
	r = requests.get("https://registry.npmjs.org/koishi-plugin-miaoscript")
	try:
		r.raise_for_status()
	except:
		logger.warn(r.text)
		
	result = r.json()
	try:
		latest = result['dist-tags']['latest']
		assert latest=='0.0.1', f"Version mismatch {latest}"
	except Exception:
		console.print_traceback(show_locals=True)
		raise
		
	pprint(result)
	      
	logger.info("[green] complete")
	
	time.sleep(30)
