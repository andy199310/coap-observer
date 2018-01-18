import logging.config
import os

from MoteConnector import MoteConnector

logging.config.fileConfig(os.path.join('logging.conf'))
log = logging.getLogger("root")

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

from cmd import Cmd

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

class CollectCLI(Cmd):

    def __init__(self):
        log.info("Starting CollectCLI")

        Cmd.__init__(self)
        self.doc_header = 'Commands: list, add, delete'
        self.prompt = '>'
        self.intro = '\nCollectCLI! Welcome!'

        self.mote_connector_lists = []

    def do_list(self, arg):
        self.stdout.write("Current observing mote: \n")
        for mote_connector in self.mote_connector_lists:
            self.stdout.write("{0}\n".format(mote_connector.getName()))
        self.stdout.write("====== End of List ===== \n")

    def do_add(self, arg):
        if not arg:
            self.stdout.write("Please provide mote's address\n")
            return
        host = arg
        # TODO check host valid
        log.info("CLI: add got [{0}]".format(host))
        moteConnector = MoteConnector(host=host, path="g/bcollect", name=host, is_observer=True, object_callback=object_callback)
        moteConnector.getName()
        moteConnector.start()
        self.mote_connector_lists.append(moteConnector)

    def do_delete(self, arg):
        if not arg:
            self.stdout.write("Please provide mote's address\n")
            return
        host = arg
        # TODO check host valid
        log.info("CLI: delete got [{0}]".format(host))
        for mote_connector in self.mote_connector_lists:
            if mote_connector.getName() == host:
                log.info("Found [{0}]. Closing!".format(host))
                mote_connector.close()
                self.mote_connector_lists.remove(mote_connector)

    def do_quit(self, arg):
        log.info("Stopping CollectCLI")
        for mote_connector in self.mote_connector_lists:
            log.info("Closing {0}!".format(mote_connector.getName()))
            mote_connector.close()
        return True

if __name__=="__main__":
    collect_cli = CollectCLI()
    collect_cli.cmdloop()
