import struct
from .exceptions import InvalidPacketException

# An RCON package looks like this:
# https://wiki.vg/RCON
#
#  1234 5678 9012 345...
# +----+----+----+--------+--+
# |LLLL|IIII|TTTT|PPPPP...|00|
# +----+----+----+--------+--+
#
# L: int -> length(ident + type + payload + padding)
# I: int -> Request ID
# T: int -> Payload Type
# P: char -> ASCII encoded payload
# 0: byte -> null padding byte


class Packet:
    """
    RCON data packet containing ident number,
    command type and payload string.

    An RCON package looks like this:
    https://wiki.vg/RCON

     1234 5678 9012 345...
    +----+----+----+--------+--+
    |LLLL|IIII|TTTT|PPPPP...|00|
    +----+----+----+--------+--+

    L: int -> length(ident + type + payload + padding)
    I: int -> Request ID
    T: int -> Payload Type
    P: char -> ASCII encoded payload
    0: byte -> null padding byte

    Raises:
        InvalidPacketException

    Arguments:
        ident {int} -- command ident number
        cmd {int} -- comamnd type
        payload {str} -- command payload
    """

    ident: int
    cmd: int
    payload: str

    def __init__(self, ident: int, cmd: int, payload: str):
        self.ident = ident
        self.cmd = cmd
        self.payload = payload

    def encode(self, charset='utf-8') -> bytes:
        """
        Encode packet into raw binary data.

        Returns:
            bytes -- raw binary packet data
        """
        data = struct.pack('<ii', self.ident, self.cmd) + \
            self.payload.encode(charset) + b'\x00\x00'
        ln = struct.pack('<i', len(data))
        return ln + data

    @staticmethod
    def decode(data: bytes, charset='utf-8') -> (object, int):
        """
        Decode packet from raw data.

        Arguments:
            data {bytes} -- raw packet data

        Raises:
            InvalidPacketException

        Returns:
            object -- decoded packet instance or None, if decoding failed or was incomplete
            int -- remaining packet length to receive when packet was incomplete
        """

        if len(data) < 14:
            return (None, 14)

        ln = struct.unpack('<i', data[:4])[0] + 4
        if len(data) < ln:
            return (None, ln)

        ident, cmd = struct.unpack('<ii', data[4:12])
        payload = data[12:-2].decode(charset)

        padding = data[-2:]
        if padding != b'\x00\x00':
            raise InvalidPacketException()

        return (Packet(ident, cmd, payload), 0)

    def __str__(self) -> str:
        return '<Packet {{ ident: {}, cmd: {}, payload: \'{}\' }}>'.format(
            self.ident, self.cmd, self.payload)
