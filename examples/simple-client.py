import asyncio
import argparse
from asyncrcon import AsyncRCON


def main():
    # Setting up command line parser and parsing arguments
    parser = argparse.ArgumentParser('rconcmd')
    parser.add_argument('--address', '-a', type=str, required=True, help='RCON address')
    parser.add_argument('--password', '-p', type=str, required=True, help='RCON password')
    argv = parser.parse_args()

    # Getting asyncio event loop to execute
    # input loop asyncronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(input_loop(argv.address, argv.password))
    loop.close()


async def input_loop(addr: str, pw: str):
    # Connecto to RCON server
    rcon = AsyncRCON(addr, pw)
    await rcon.open_connection()

    print('Connected to {}.'.format(addr))

    while True:
        # Getting command input
        inpt = input('> ')

        if not inpt:
            continue

        # Check if user wants to quit console
        if inpt.lower() in ['q', 'e', 'exit', 'quit']:
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
