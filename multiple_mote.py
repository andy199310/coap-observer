import logging.config
import os
logging.config.fileConfig(os.path.join('logging.conf'))
log = logging.getLogger("root")

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
engine = create_engine('mysql+mysqlconnector://{username}:{password}@{host}/{database}'.format(username=config.get('database', 'username'),
                                                                                               password=config.get('database', 'password'),
                                                                                               host=config.get('database', 'host'),
                                                                                               database=config.get('database', 'database'),
                                                                                               ), echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

hosts = [
    # "fd00::212:4b00:615:a6dd", # root
    "fd00::212:4b00:615:a620",
]

from MoteConnector import MoteConnector


def object_callback(mote_data):
    try:
        log.info("Got new object_callback")
        log.debug(mote_data)
        session = Session()
        session.add(mote_data)
        session.commit()
    except:
        log.error("Got Error!")
        import sys
        log.critical("Unexpected error:{0}".format(sys.exc_info()[0]))
        log.critical("Unexpected error:{0}".format(sys.exc_info()[1]))


mote_connector_lists = []

for host in hosts:
    moteConnector = MoteConnector(host=host, path="g/bcollect", name=host, is_observer=True, object_callback=object_callback)
    moteConnector.start()
    mote_connector_lists.append(moteConnector)
