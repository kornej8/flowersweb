#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flowerweb")
sys.path.insert(0, "/var/www/flowerweb/flowerweb/flowerweb/lib/python3.11/site-packages")
from flowerweb.main import application
