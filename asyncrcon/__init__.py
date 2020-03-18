"""
asyncrcon is a client side implementation of the Minecraft RCON protocol
using asyncio sockets for non-blocing socket handling.

# Links

- [**Docs**](https://zekroTJA.github.io/asyncrcon)
- [**Source Code**](https://github.com/zekroTJA/asyncrcon)
- [**Examples**](https://github.com/zekroTJA/asyncrcon/tree/master/examples)
- [**License**](https://github.com/zekroTJA/asyncrcon/tree/master/LICENSE)

# Usage Example

For more examples, see [**here**](https://github.com/zekroTJA/asyncrcon/tree/master/examples).

Here, we are opening a RCON connection to add a given user to the servers whitelist. Then, we close the connection.

    from asyncrcon import AsyncRCON, AuthenticationException

    async def add_to_whitelist(user: str):
        rcon = AsyncRCON('loclahost:25575', 'secretRCONPassword')
        try:
            await rcon.open_connection()
        except AuthenticationException:
            print('Login failed: Unauthorized.')
            return

        res = await rcon.command('whitelist add {}'.format(user))
        print(res)

        rcon.close()
"""

# flake8: noqa

__title__     = 'asyncrcon'
__aurhot__    = 'zekro'
__version__   = '1.1.3'
__licence__   = 'Apache Licence 2.0'
__copyright__ = '(c) 2020 Ringo Hoffmann (zekro Development)'
__url__       = 'https://github.com/zekroTJA/asyncrcon'


from .rcon import *
from .packet import *
from .exceptions import *
