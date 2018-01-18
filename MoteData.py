import logging
log = logging.getLogger("moteData")

import struct
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class MoteData(Base):
    __tablename__ = 'mote_data'

    id = Column(Integer, primary_key=True)
    mote = Column(String(200))
    start_asn = Column(Integer)
    end_asn = Column(Integer)
    event_counter = Column(Integer)
    event_threshold = Column(Integer)
    event_threshold_last_change = Column(Integer)
    packet_counter = Column(Integer)
    parent_address = Column(String(10))
    rank = Column(Integer)
    parent_link_etx = Column(Integer)
    parent_link_rssi = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __str__(self):
        output = []
        output += ['mote    : {0}'.format(self.mote)]
        output += ['startAsn: {0}'.format(self.start_asn)]
        output += ['endAsn  : {0}'.format(self.end_asn)]
        output += ['ec      : {0}'.format(self.event_counter)]
        output += ['et      : {0}'.format(self.event_threshold)]
        output += ['etlc    : {0}'.format(self.event_threshold_last_change)]
        output += ['pc      : {0}'.format(self.packet_counter)]
        output += ['parent  : {0}'.format(self.parent_address)]
        output += ['rank    : {0}'.format(self.rank)]
        output += ['p_etx   : {0}'.format(self.parent_link_etx)]
        output += ['p_rssi  : {0}'.format(self.parent_link_rssi)]
        return '\n'.join(output)

    @classmethod
    def make_from_bytes(cls, mote, data):
        packet_format = [
            "<xx",  # start_flag
            "xx",   # alignment_padding[2]
            "I",    # start_asn
            "I",    # end_asn
            "I",    # event_counter
            "B",    # event_threshold
            "xxx",  # alignment_padding[3]
            "I",    # event_threshold_last_change
            "I",    # packet_counter
            "cc",   # parent_address
            "H",    # rank
            "H",    # parent_link_etx
            "h",    # parent_link_rssi
            "xx",   # end_flag[2]
            "xx",   # end_alignment_padding[2]
        ]
        packet_format_str = ''.join(packet_format)
        packet_item = struct.unpack(packet_format_str, data)
        mote_data = MoteData(
            mote=mote,
            start_asn=packet_item[0],
            end_asn=packet_item[1],
            event_counter=packet_item[2],
            event_threshold=packet_item[3],
            event_threshold_last_change=packet_item[4],
            packet_counter=packet_item[5],
            parent_address="".join("{:02x}".format(ord(c)) for c in packet_item[6:8]),
            rank=packet_item[8],
            parent_link_etx=packet_item[9],
            parent_link_rssi=packet_item[10],
        )
        return mote_data
