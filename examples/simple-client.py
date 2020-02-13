import asyncio
import argparse
import logging
from asyncrcon import AsyncRCON, AuthenticationException


def main():
    # Setting up command line parser and parsing arguments
    parser = argparse.ArgumentParser('rconcmd')
    parser.add_argument('--address', '-a', type=str, required=True, help='RCON address')
    parser.add_argument('--password', '-p', type=str, required=True, help='RCON password')
    parser.add_argument('--log-level', '-l', type=int, default=20, help='Log Level')
    argv = parser.parse_args()

    logging.basicConfig(
        level=argv.log_level,
        format='%(levelname)s | %(name)s | %(message)s')

    # Getting asyncio event loop to execute
    # input loop asyncronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(input_loop(argv.address, argv.password))
    loop.close()


async def input_loop(addr: str, pw: str):
    # Connecto to RCON server
    rcon = AsyncRCON(addr, pw)
    try:
        await rcon.open_connection()
    except AuthenticationException:
        print('Login failed: Unauthorized.')
        return

    print('Connected to {}.'.format(addr))

    while True:
        # Getting command input
        inpt = input('> ')

        if not inpt:
            continue

        # Check if user wants to quit console
        if inpt.lower() in ['q', 'e', 'exit', 'quit']:
            rcon.close()
            print('Bye.')
            break

        # Executing command and getting response
        res = await rcon.command(inpt)
        # Print response
        print(res)

    # Close RCON connection on quit
    rcon.close()

if __name__ == '__main__':
    main()
