import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/EEE4022S/code/modules')
from io import BytesIO
from bitcoin.rpc import RawProxy
import tx
from tx import Tx


p = RawProxy(service_port = 18332)
tx_id = sys.argv[1]
raw_tx = bytes.fromhex(p.getrawtransaction(tx_id))
stream = BytesIO(raw_tx)
tx = Tx.parse(stream, testnet = True)

print(tx)

