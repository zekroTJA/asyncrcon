"""
# asyncrcon

asyncrcon is a client side implementation of the Minecraft RCON protocol
using asyncio sockets for non-blocing socket handling.
"""

# flake8: noqa

__title__     = 'asyncrcon'
__aurhot__    = 'zekro'
__version__   = '1.0.0'
__licence__   = 'Apache Licence 2.0'
__copyright__ = '(c) 2020 Ringo Hoffmann (zekro Development)'
__url__       = 'https://github.com/zekroTJA/async-rcon'


from .rcon import *
from .packet import *
from .exceptions import *
