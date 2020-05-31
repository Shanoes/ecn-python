import asyncio
import logging
import sys
from asyncua import Client, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)


async def main():
    url = "opc.tcp://mx80_ua:4840"
    prefix = "ns=2;s=0:"
    arglen = len(sys.argv)

    if arglen > 1:
        url = sys.argv[1]
        _logger.info("url: %r", url)
 

    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        # _logger.info("Objects node is: %r", client.nodes.objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        # _logger.info("Children of root are: %r", await client.nodes.root.get_children())

        if arglen > 2:
            handler = SubHandler()
            handle = None
            sub = await client.create_subscription(500, handler)
            tags = sys.argv[2:]
            for tag in tags:
                _logger.info("TAG FOUND: %r", prefix + tag)
                node = client.get_node(prefix + tag) 
                print(node)
                handle = await sub.subscribe_data_change(node)

            await sub.subscribe_events()

            await asyncio.sleep(60)

            await sub.unsubscribe(handle)
            await sub.delete()

if __name__ == "__main__":
    asyncio.run(main())
