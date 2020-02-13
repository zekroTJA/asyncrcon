import asyncio
import logging
from typing import Optional
from asyncio import StreamReader, StreamWriter
from .packet import Packet
from .exceptions import \
    AuthenticationException, NulLResponseException, MaxRetriesExceedException


_DEFAULT_RCON_PORT = 25575
_CMD_LOGIN = 3
_CMD_RUN = 2
_CMD_RESPONSE = 0


class AsyncRCON:
    """
    Handles RCON TCP connection and command sending
    and receiving.

    Raises:
        AuthenticationException
        NulLResponseException

    Arguments:
        addr {str} -- RCON server address and port (i.e.: localhost, localhost:25575, 1.2.3.4:6543)
        passwd {str} -- RCON authentication password

    Keyword Arguments:
        max_command_retries {Optional[int]} -- Maximum ammount of failed command retries (default: {10})
    """

    _addr: str
    _port: int
    _passwd: str
    _max_command_retries: int
    _auto_reconnect: bool

    _writer: StreamWriter
    _reader: StreamReader

    _logger: logging.Logger

    def __init__(self, addr: str, passwd: str,
                 max_command_retries: Optional[int] = 10,
                 auto_reconnect: Optional[bool] = True):
        self._passwd = passwd
        addr_split = addr.split(':', 1)
        self._addr = addr_split[0]
        self._port = int(addr_split[1]) if len(addr_split) > 1 \
            else _DEFAULT_RCON_PORT
        self._max_command_retries = max_command_retries
        self._auto_reconnect = auto_reconnect
        self._logger = logging.getLogger('asyncrcon')

    async def open_connection(self):
        """|coro|
        Open connection event loop and log
        in to the RCON server.

        Raises:
            AuthenticationException
        """

        self._reader, self._writer = await asyncio.open_connection(
            self._addr, self._port)

        self._send(Packet(0, _CMD_LOGIN, self._passwd))

        packet = await self._receive()

        if packet.ident == -1:
            raise AuthenticationException

    async def command(self, cmd: str) -> str:
        """|coro|
        Execute a command over RCON and wait
        for response. If the command reponse is
        empty or erroeus

        Arguments:
            cmd {str} -- command literal

        Raises:
            MaxRetriesExceedException

        Returns:
            str -- RCON server response (may be empty in some cases)
        """
        self._send_command(cmd)

        for _ in range(0, 10):
            try:
                return await self._rec_command()
            except NulLResponseException:
                self.close()
                await self.open_connection()
                self._send_command(cmd)
                continue

        raise MaxRetriesExceedException

    def close(self):
        """
        Close the socket connection to the
        RCON server.
        """

        self._writer.close()

    def _send_command(self, cmd: str):
        """
        Command sending wrapper.
        Sends the actual command package and another
        invalid package to trigger reponse with ident
        '0' to register end of response from the server.

        Arguments:
            cmd {str} -- command literal
        """
        self._send(Packet(0, _CMD_RUN, cmd))
        self._send(Packet(1, _CMD_RESPONSE, ''))

    async def _rec_command(self) -> str:
        """|coro|
        Receive multi-packet command response.

        Returns:
            str -- command response
        """

        res = ''
        while True:
            packet = await self._receive()
            if packet.ident != 0:
                break
            res += packet.payload
        return res

    async def _receive(self) -> Packet:
        """|coro|
        Receive single packet.

        Raises:
            NulLResponseException

        Returns:
            Packet -- response data packet
        """

        data = b''
        self._logger.debug('--> start rec')
        while True:
            packet, ln = Packet.decode(data)
            if packet:
                self._logger.debug('--> finished rec')
                return packet

            while len(data) < ln:
                try:
                    data += await self._reader.read(ln - len(data))
                except OSError as e:
                    if not self._auto_reconnect:
                        raise e
                    self._logger.warning('Connection was closed. Try reconnecting...')
                    self.close()
                    await self.open_connection()

                if len(data) == 0:
                    raise NulLResponseException()

                self._logger.debug('package {}, {}, {}'.format(data, len(data), ln))

    def _send(self, packet: Packet):
        """
        Send encoded data packet.

        Arguments:
            packet {Packet} -- data packet
        """
        self._logger.debug('<-- send {}'.format(packet.payload))
        self._writer.write(packet.encode())
