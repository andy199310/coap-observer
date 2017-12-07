import logging.config
import os
logging.config.fileConfig(os.path.join('logging.conf'))
log = logging.getLogger("root")

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+mysqlconnector://{username}:{password}@{host}/{database}'.format(username=config.get('database', 'username'),
                                                                                               password=config.get('database', 'password'),
                                                                                               host=config.get('database', 'host'),
                                                                                               database=config.get('database', 'database'),
                                                                                               ), echo=False)
Session = sessionmaker(bind=engine)
session = Session()

hosts = [
    # "fd00::212:4b00:615:a6dd", # root
    "fd00::212:4b00:615:a620",
    "fd00::212:4b00:615:a6ff",
    "fd00::212:4b00:615:a6e2",
]

from MoteConnector import MoteConnector


def object_callback(mote_data):
    log.info("Got new object_callback")
    session.add(mote_data)
    session.commit()


mote_connector_lists = []

for host in hosts:
    moteConnector = MoteConnector(host=host, path="g/bcollect", name=host[-4:], is_observer=False, object_callback=object_callback)
    moteConnector.start()
    mote_connector_lists.append(moteConnector)
