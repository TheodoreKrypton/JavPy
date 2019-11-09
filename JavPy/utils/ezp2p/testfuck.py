import asyncio
from pybtracker import TrackerClient


async def announce():
    client = TrackerClient(
        announce_uri="udp://ipv4.tracker.harry.lu:80/announce", loop=loop
    )
    await client.start()
    peers = await client.announce(
        b"1C87017E8F18B935BABF9A9B3ECCFA64419407AD",  # infohash
        10000,  # downloaded
        40000,  # left
        5000,  # uploaded
        0,  # event (0=none)
        120,  # number of peers wanted
    )
    print(peers)


loop = asyncio.get_event_loop()
loop.run_until_complete(announce())
