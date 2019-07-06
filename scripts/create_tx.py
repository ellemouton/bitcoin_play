
import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/EEE4022S/code/modules')
from io import BytesIO
from bitcoin.rpc import RawProxy
import ecc
import helper
import tx
import script
from ecc import PrivateKey
from helper import hash256, little_endian_to_int, decode_base58, SIGHASH_ALL
from tx import Tx, TxIn, TxOut
from script import p2pkh_script, Script

def createAddress(passphrase):
    secret = little_endian_to_int(hash256(passphrase))
    publicKey = PrivateKey(secret).point
    address = publicKey.address(testnet=True)
    return address

def is_unspent(txid, index, proxy):
    return proxy.gettxout(txid, index)==None


p = RawProxy(service_port = 18332)

# Sender Information
sender_secret = b'elle.mouton@gmail.com Tranquility Cracks is a hidden gem that many seek but few find'
secret = little_endian_to_int(hash256(sender_secret))
private_key = PrivateKey(secret)
public_key = private_key.point
sender_address = public_key.address(testnet=True)

# Receiver Information
receiver_address = createAddress(b'some salt for this receiver address')

# What is in our wallet that we can spend? (this one has 0.01 tBTC)
tx_in_id = 'acf22005638e60379aa43d4cd2a5eb47a0fa1fefc5883eecf83329a607431d50'
tx_in_index = 1
tx_input = TxIn(bytes.fromhex(tx_in_id), tx_in_index)

# Checking spentness of the inputs. Should be False
print("Spentness of input "+str(tx_in_index)+": " + str(is_unspent(tx_in_id,tx_in_index, p)))

# How much BTC?
sat_in_bit = 100000000
fee = 0.0001 * sat_in_bit
input_amount = tx_input.value(testnet=True)

#creating the target output
target_amount = int(0.005 * sat_in_bit)
target_h160 = decode_base58(sender_address)
target_script = p2pkh_script(target_h160)
target_output = TxOut(amount = target_amount, script_pubkey = target_script)

#creating the change output
change_amount = int(input_amount - target_amount - fee)
change_160 = decode_base58(receiver_address)
change_script = p2pkh_script(change_160)
change_output = TxOut(amount = change_amount, script_pubkey = change_script)

#create the Tx object
tx_obj = Tx(1, [tx_input], [change_output, target_output], 0, True)


#signing the transaction
z = tx_obj.sig_hash(0) #get sig_hash of the first input
der = private_key.sign(z).der()
sig = der + SIGHASH_ALL.to_bytes(1, 'big')
sec = public_key.sec()
script_sig = Script([sig, sec])
tx_obj.tx_ins[0].script_sig = script_sig
print(tx_obj.serialize().hex())

print(sender_address)
print(receiver_address)


