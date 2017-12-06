import logging.config
import os
from coapthon.client.helperclient import HelperClient
from MoteData import MoteData

logging.config.fileConfig(os.path.join('logging.conf'))
log = logging.getLogger("root")

host = "fd00::202:2:2:2"


def message_callback(response):
    log.debug("Got new message")
    if log.isEnabledFor(logging.DEBUG):
        packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
        log.debug(packet_content)

    log.debug("Payload length: {0}".format(len(response.payload)))
    mote_data = MoteData.make_from_bytes(response.source[0], response.payload)
    log.debug("=================================")
    coapClient.stop()

coapClient = HelperClient(server=(host, 5683))
coapClient.get(path="g/bcollect", callback=message_callback)
coapClient.stop()
