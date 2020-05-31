import sys
import time
from opcua import Client, ua

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


if __name__ == "__main__":
    url = "opc.tcp://mx80_ua:4840"
    prefix = "ns=2;s=0:"
    arglen = len(sys.argv)

    if arglen > 1:
        url = sys.argv[1]
        print("url: %r", url)
 
        client = Client(url)
        try:
            client.connect()
            client.load_type_definitions()  # load definition of server specific structures/extension objects


            # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
            root = client.get_root_node()
            print("Root node is: ", root)
            
            objects = client.get_objects_node()
            print("Objects node is: ", objects)

            # Node objects have methods to read and write node attributes as well as browse or populate address space
            print("Children of root are: ", root.get_children())

            if arglen > 2:
                handler = SubHandler()
                handle = None
                sub = client.create_subscription(500, handler)
                tags = sys.argv[2:]
                for tag in tags:
                    print("TAG FOUND: %r", prefix + tag)
                    node = client.get_node(prefix + tag) 
                    print(node)
                    handle = sub.subscribe_data_change(node)

                sub.subscribe_events()

                time.sleep(60)

                sub.unsubscribe(handle)
                sub.delete()

        finally:
            client.disconnect()