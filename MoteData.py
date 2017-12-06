import logging
log = logging.getLogger("moteData")

import struct


class MoteData:
    def __init__(self, mote, event_counter, event_threshold, event_threshold_last_change, packet_counter, parent_address):
        self.mote = mote
        self.event_counter = event_counter
        self.event_threshold = event_threshold
        self.event_threshold_last_change = event_threshold_last_change
        self.packet_counter = packet_counter
        self.parent_address = parent_address

    def __str__(self):
        return "ec: {0}, et: {1}, etlc: {2}, pc: {3}".format(self.event_counter, self.event_threshold, self.event_threshold_last_change, self.packet_counter)

    @classmethod
    def make_from_bytes(cls, mote, data):
        packet_format = [
            "<xx",  # start_flag
            "xx",   # alignment_padding[2]
            "I",    # event_counter
            "B",    # event_threshold
            "xxx",  # alignment_padding[3]
            "I",    # event_threshold_last_change
            "I",    # packet_counter
            "cc",   # parent_address
            "xx",   # end_flag[2]
        ]
        packet_format_str = ''.join(packet_format)
        packet_item = struct.unpack(packet_format_str, data)
        mote_data = MoteData(
            mote=mote,
            event_counter=packet_item[0],
            event_threshold=packet_item[1],
            event_threshold_last_change=packet_item[2],
            packet_counter=packet_item[3],
            parent_address="".join("{:02x}".format(ord(c)) for c in packet_item[4:6])
        )
        return mote_data
