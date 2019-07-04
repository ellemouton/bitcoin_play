#only works with Python 3.5 and greater

import binascii
import asyncio
import zmq
import zmq.asyncio
import signal
import struct
import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/EEE4022S/code/modules')
from io import BytesIO
from bitcoin.rpc import RawProxy
import tx
from tx import Tx

port = 28333

def printInfo(rawtx):
    raw_tx = bytes.fromhex(rawtx)
    stream = BytesIO(raw_tx)
    tx = Tx.parse(stream, testnet = True)
    print(tx)

class ZMQHandler():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.zmqContext = zmq.asyncio.Context()

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt(zmq.RCVHWM, 0)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
        self.zmqSubSocket.connect("tcp://127.0.0.1:%i" % port)

    async def handle(self) :
        msg = await self.zmqSubSocket.recv_multipart()
        topic = msg[0]
        body = msg[1]
        sequence = "Unknown"
        if len(msg[-1]) == 4:
          msgSequence = struct.unpack('<I', msg[-1])[-1]
          sequence = str(msgSequence)

        if topic == b"rawtx":
            rawtxid = str(binascii.hexlify(body))
            rawtxid = rawtxid[2:len(rawtxid)-1]
            printInfo(rawtxid)

        # schedule ourselves to receive the next message
        asyncio.ensure_future(self.handle())

    def start(self):
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.create_task(self.handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.zmqContext.destroy()


#connect to bitcoin-cli
p = RawProxy(service_port=18332)

daemon = ZMQHandler()
daemon.start()



