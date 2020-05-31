import asyncio
import logging

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
    url = "opc.tcp://192.168.1.200:4840"
    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        _logger.info("Children of root are: %r", await client.nodes.root.get_children())

        # uri = "http://examples.freeopcua.github.io"
        # idx = await client.get_namespace_index(uri)
        # _logger.info("index of our namespace is %s", idx)
        # get a specific node knowing its node id
        # var = client.get_node(ua.NodeId(1002, 2))
        tank1level = client.get_node("ns=2;s=0:TANK1_LEVEL")
        print(tank1level)
        # await var.read_data_value()  # get value of node as a DataValue object
        #value = await var.read_value()  # get value of node as a python builtin
        # _logger.info("myvar is: %r", value)
        tank2flow = client.get_node("ns=2;s=0:TANK2_FLOW")
        dv = ua.DataValue(ua.Variant(1.2, ua.VariantType.Float))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        await tank2flow.set_value(dv)

        valve1Open = client.get_node("ns=2;s=0:VALVE1_OPEN")
        dv = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        await valve1Open.set_value(dv)
        # await tank2flow.write_value(ua.Variant([23.0], ua.VariantType.Float)) #set node value using explicit data type
        # await tank2flow.write_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        # myvar = await client.nodes.root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
        # obj = await client.nodes.root.get_child(["0:Objects", "2:MyObject"])
        #_logger.info("myvar is: %r", myvar)

        # subscribing to a variable node
        handler = SubHandler()
        sub = await client.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(tank1level)
        await asyncio.sleep(5)


        # we can also subscribe to events from server
        await sub.subscribe_events()
        await sub.unsubscribe(handle)
        await sub.delete()

        # calling a method on server
        # res = await obj.call_method("2:multiply", 3, "klk")
        #_logger.info("method result is: %r", res)


if __name__ == "__main__":
    asyncio.run(main())
