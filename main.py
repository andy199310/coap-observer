import logging.config
import os
from coapthon.client.helperclient import HelperClient
from MoteData import MoteData

logging.config.fileConfig(os.path.join('logging.conf'))
logger = logging.getLogger("root")

host = "fd00::202:2:2:2"


def message_callback(response):
    logger.debug("Got new message")
    if logger.isEnabledFor(logging.DEBUG):
        packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
        logger.debug(packet_content)

    logger.debug("Payload length: {0}".format(len(response.payload)))
    mote_data = MoteData.make_from_bytes(response.payload)
    logger.debug("=================================")

coapClient = HelperClient(server=(host, 5683))
coapClient.get(path="g/bcollect", callback=message_callback)
