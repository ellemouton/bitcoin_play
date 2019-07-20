import sys
sys.path.insert(0, '/Users/ellemouton/Documents/2019/Sem2/EEE4022S/code/modules')
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
from script import p2pkh_script, p2sh_script, Script

''' Connect to bitcoind'''
p = RawProxy(service_port = 18332)

''' Global Variables '''
sat_in_bit = 100000000

''' Functions '''
def is_unspent(txid, index):
    return p.gettxout(txid, index)==None

def get_input_info(num_inputs):
    tx_ins = []
    amount_available = 0

    for i in range(num_inputs):
        temp_id = input("Enter prev_tx_id for input "+str(i+1)+": ")
        temp_index =  int(input("Enter prev_tx_index for input "+str(i+1)+": "))

        if(is_unspent(temp_id, temp_index)):
            print("Tx had already been spent. Not good.")
        else:
            print("Tx is Unspent. All good.")
            tx_ins.append(TxIn(bytes.fromhex(temp_id), temp_index))
            amount_available += tx_ins[i].value(testnet=True)

    return tx_ins, amount_available

def determine_fee(input_amount):
    valid = False

    while(valid == False):
        fee_amount = int(float(input("Fee amount (in tBTC)? ")) * sat_in_bit)

        if(fee_amount > input_amount):
            print("Insufficient Funds")
        else:
            valid = True
            print("Sufficient Funds")

    return input_amount - fee_amount

def get_output_info(num_outputs, amount_available):
    tx_outs = []
    amount = amount_available

    for i in range(num_outputs):
        target_address = input("Enter address of recipient: ")
        target_h160 = decode_base58(target_address)
        valid_amount = False
        target_amount = int(float(input("How much would you like to pay them (in tBTC)?  ")) * sat_in_bit)

        while(valid_amount  == False):

            if(target_amount > amount):
                print("Insufficient Funds")
                target_amount = int(float(input("How much would you like to pay them (in tBTC)?  ")) * sat_in_bit)
            else:
                print("Sufficient Funds")
                valid_amount = True

        amount = amount - target_amount
        print(str(amount/sat_in_bit)+" tBTC remaining")

        if(target_address[0]=='2'):
            print("This recipient is a P2SH")
            target_script = p2sh_script(target_h160)
            tx_outs.append(TxOut(amount = target_amount, script_pubkey = target_script))
        else:
            print("This recipient is a P2PKH")
            target_script = p2pkh_script(target_h160)
            tx_outs.append(TxOut(amount = target_amount, script_pubkey = target_script))


    if(amount > 0):
        print("There is a remainder of "+str(amount/sat_in_bit)+" tBTC. Please fill in recipient details:")

        target_address = input("Enter address of recipient: ")
        target_h160 = decode_base58(target_address)
        target_amount = amount

        if(target_address[0]=='2'):
            print("This recipient is a P2SH")
            target_script = p2sh_script(target_h160)
            tx_outd.append(TxOut(amount = target_amount, script_pubkey = target_script))
        else:
            print("This recipient is a P2PKH")
            target_script = p2pkh_script(target_h160)
            tx_outs.append(TxOut(amount = target_amount, script_pubkey = target_script))

    return tx_outs

def get_keys_for_input(index):
    print("Enter your private key passphrase to prove that you can sign input "+str(index)+":")
    password = getpass.getpass('Passphrase:')
    secret = little_endian_to_int(hash256(str.encode(password)))
    private_key = PrivateKey(secret)
    public_key = private_key.point
    sender_address = public_key.address(testnet=True)
    print("Address corresponding to entered passphrase: " + sender_address)
    return private_key, public_key


''' Construct Inputs '''
num_inputs = int(input("How many inputs? "))
tx_ins, input_amount = get_input_info(num_inputs)

print("Amount available to spend (before fees): " +str(input_amount/sat_in_bit) + " tBTC")

''' Fee '''
amount_available = determine_fee(input_amount)
print("Amount available to spend (after fees): " +str(amount_available/sat_in_bit) + " tBTC")

''' Construct Outputs '''
tx_outs = []
num_outputs= int(input("How many outputs (NOT including the output for left-over change)? "))
tx_outs  = get_output_info(num_outputs, amount_available)

''' Construct Transaction object '''
tx_obj = Tx(1, tx_ins, tx_outs, 0, True)


''' Signing the inputs '''
for i in range(len(tx_ins)):
    z = tx_obj.sig_hash(i)

    private_key, public_key = get_keys_for_input(i)

    der = private_key.sign(z).der()
    sig = der + SIGHASH_ALL.to_bytes(1, 'big')
    sec = public_key.sec()
    script_sig = Script([sig, sec])
    tx_obj.tx_ins[i].script_sig = script_sig



if(tx_obj.verify()):
    print("-------Transaction Successfully Signed-------")
    print("===>raw transaction:")
    tx_serial = tx_obj.serialize().hex()
    print(tx_serial)
    #p.sendrawtransaction(tx_serial)
    #print("===>transaction successfully published<====")
    print("==> use this with 'bitcoin-cli sendrawtransaction <raw_tx>' in order to broadcast it")
else:
    print("Incorrect Signature for this Transaction")

































