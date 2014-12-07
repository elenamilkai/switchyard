import struct
from enum import Enum

from switchyard.lib.packet.packet import PacketHeaderBase,Packet
from switchyard.lib.address import SpecialIPv4Address, IPv4Address


'''
References:
    IETF RFC 2453
'''

class RIPCommand(Enum):
    Request = 1
    Reply = 2

class RIPRouteEntry(PacketHeaderBase):
    __slots__ = ('_family','_tag','_addr','_mask','_nexthop','_metric')
    _PACKFMT = '!HHIIII'
    _MINLEN = struct.calcsize(_PACKFMT)

    def __init__(self):
        self.family = 2
        self.tag = 0
        self.addr = SpecialIPv4Address.INADDR_ANY
        self.mask = SpecialIPv4Address.INADDR_ANY
        self.nexthop = SpecialIPv4Address.INADDR_ANY
        self.metric = 16

    def size(self):
        return RIPRouteEntry._MINLEN

    def to_bytes(self):
        return struct.pack(RIPRouteEntry._PACKFMT, self.family, self.tag,
                           int(self.addr), int(self.mask), int(self.nexthop),
                           self.metric)

    def from_bytes(self, raw):
        pass

    # FIXME properties

class RIPv2(PacketHeaderBase):
    __slots__ = ('_command','_version','_domain','_routes')
    _PACKFMT = '!BBH'
    _MINLEN = struct.calcsize(_PACKFMT)

    def __init__(self):
        self.command = RIPCommand.Request
        self.version = 2
        self.domain = 0

    def size(self):
        return len(self.to_bytes())

    def to_bytes(self):
        '''
        Return packed byte representation of the UDP header.
        '''
        hdr = struct.pack(RIPv2._PACKFMT, self.command, self.version, self.domain)
        routes = b''.join([r.to_bytes() for r in self._routes])
        return hdr + routes

    def from_bytes(self, raw):
        FIXME

    def __eq__(self, other):
        FIXME

    def __str__(self):
        FIXME

    def next_header_class(self):
        return None

    def pre_serialize(self, raw, pkt, i):
        pass
