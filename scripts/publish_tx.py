import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/EEE4022S/code/modules')
from io import BytesIO
from bitcoin.rpc import RawProxy
import ecc
import helper
import tx
import script
import getpass
from ecc import PrivateKey
from helper import hash256, little_endian_to_int, decode_base58, SIGHASH_ALL
from tx import Tx, TxIn, TxOut
from script import p2pkh_script, Script

sat_in_bit = 100000000

# connect to bitcoind
p = RawProxy(service_port = 18332)

def is_unspent(txid, index):
    return p.gettxout(txid, index)==None





tx_ins = []
amount_available = 0


# Get info for TxIns from user
num_inputs = int(input("How many inputs? "))

for i in range(num_inputs):
    temp_id = input("Enter prev_tx_id for input "+str(i+1)+": ")
    temp_index =  int(input("Enter prev_tx_index for input "+str(i+1)+": "))

    if(is_unspent(temp_id, temp_index)):
        print("Tx had already been spent. Not good.")
    else:
        print("Tx is Unspent. All good.")
        tx_ins.append(TxIn(bytes.fromhex(temp_id), temp_index))
        amount_available += tx_ins[i].value(testnet=True)

print("\nAmount available to spend: " +str(amount_available/sat_in_bit) + " tBTC\n")

# Get target amount and fee info

target_amount = 0
fee_amount = 0
amounts_valid = False

while(amounts_valid == False):
    target_amount = int(float(input("How much would you like to pay (in tBTC)?  ")) * sat_in_bit)
    fee_amount = int(float(input("Fee amount (in tBTC)? ")) * sat_in_bit)

    if(target_amount+fee_amount > amount_available):
        print("Insufficient Funds")
    else:
        amounts_valid = True
        print("Sufficient Funds")


# get target address
target_address = input("Enter address of recipient: ")
target_h160 = decode_base58(target_address)
target_script = p2pkh_script(target_h160)
target_output = TxOut(amount = target_amount, script_pubkey = target_script)


# Sender Information
print("Enter your private key passphrase to prove that you can sign the inputs:")
password = getpass.getpass('Passphrase:')
secret = little_endian_to_int(hash256(str.encode(password)))
private_key = PrivateKey(secret)
public_key = private_key.point
sender_address = public_key.address(testnet=True)
print("Your Address: " + sender_address)

#send change back to sender
change_amount = int(amount_available - target_amount - fee_amount)
change_160 = decode_base58(sender_address)
change_script = p2pkh_script(change_160)
change_output = TxOut(amount = change_amount, script_pubkey = change_script)

#create the Tx object
tx_obj = Tx(1, tx_ins, [change_output, target_output], 0, True)

#signing the transaction
for i in range(len(tx_ins)):
    z = tx_obj.sig_hash(i)
    der = private_key.sign(z).der()
    sig = der + SIGHASH_ALL.to_bytes(1, 'big')
    sec = public_key.sec()
    script_sig = Script([sig, sec])
    tx_obj.tx_ins[i].script_sig = script_sig


if(tx_obj.verify()):
    print("-------Transaction Successfully Signed-------")
    print("===>publishing the following transaction:")
    tx_serial = tx_obj.serialize().hex()
    print(tx_serial)
    p.sendrawtransaction(tx_serial)
    print("===>transaction successfully published<====")
else:
    print("Incorrect Signature for this Transaction")









