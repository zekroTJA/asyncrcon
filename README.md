# asyncrcon
[![PyPI](https://img.shields.io/pypi/v/asyncrcon)](https://pypi.org/project/asyncrcon/)&nbsp;[![](https://img.shields.io/badge/docs-passing-brightgreen)](https://zekroTJA.github.io/asyncrcon)

asyncrcon is a client side implementation of the Minecraft RCON protocol
using asyncio sockets for non-blocing socket handling.

```
pip install asyncrcon
```

# Links

- [**Docs**](https://zekroTJA.github.io/asyncrcon)
- [**Source Code**](https://github.com/zekroTJA/asyncrcon)
- [**Examples**](https://github.com/zekroTJA/asyncrcon/tree/master/examples)
- [**License**](https://github.com/zekroTJA/asyncrcon/tree/master/LICENSE)

# Usage Example

For more examples, see [**here**](https://github.com/zekroTJA/asyncrcon/tree/master/examples).
Here, we are opening a RCON connection to add a given user to the servers whitelist. Then, we close the connection.

```py
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
```

---

© 2020 Ringo Hoffmann (zekro Development)  
Covered by the Apache Licence 2.0. 
