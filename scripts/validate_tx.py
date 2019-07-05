import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/EEE4022S/code/modules')
from io import BytesIO
from bitcoin.rpc import RawProxy
import tx
from tx import Tx


def is_unspent(txid, index, proxy):
    return proxy.gettxout(txid, index)==None


p = RawProxy(service_port = 18332)
tx_id = sys.argv[1]
raw_tx = bytes.fromhex(p.getrawtransaction(tx_id))
stream = BytesIO(raw_tx)
tx = Tx.parse(stream, testnet = True)

print(tx)

print('****** Starting Validation of the Tx ******')

#1: Checking spentness of the inputs. If checking an existing tx then all should be True (all spent)
for i, tx_in in enumerate(tx.tx_ins, start = 0):
    print("Spentness of input "+str(i)+": "+str(is_unspent(tx_in.prev_tx.hex(),tx_in.prev_index, p)))


#2: Checkthe sum of the inputs vs outputs (ie that fee is non negative)
print("Fee is positive: "+str(tx.fee()>=0))

#3: Checking the signiture
print("Valid ScriptSigs: "+str(tx.verify()))

print('*******************************************')

