from MoteConnector import MoteConnector

import logging.config
import os
logging.config.fileConfig(os.path.join('logging.conf'))
log = logging.getLogger("root")

hosts = [
    "fd00::202:2:2:2",
    "fd00::203:3:3:3",
]

for host in hosts:
    moteConnector = MoteConnector(host=host, path="g/bcollect", name=host[-4:], is_observer=True)
    moteConnector.start()
