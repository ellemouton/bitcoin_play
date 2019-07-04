import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/EEE4022S/code/modules')
from io import BytesIO
from bitcoin.rpc import RawProxy
import ecc
import helper
import tx
import script
from ecc import PrivateKey
from helper import hash256, little_endian_to_int
from tx import Tx

def createAddress(passphrase):
    secret = little_endian_to_int(hash256(passphrase))
    publicKey = PrivateKey(secret).point
    address = publicKey.address(testnet=True)
    return address


passphrase = b'elle.mouton@gmail.com Tranquility Cracks is a hidden gem that many seek but few find'
address = createAddress(passphrase)

p = RawProxy(service_port = 18332)
raw_tx = p.getrawtransaction('3e459a708c653470323968b4273d7e304eb22a328db56901a5fc977bc783b72d')
tx_raw = bytes.fromhex(raw_tx)
stream = BytesIO(tx_raw)
txo = Tx.parse(stream, testnet = True)

print(txo)
print('fee: ' + str(txo.fee()))

