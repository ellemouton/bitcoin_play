import sys
from bitcoin.rpc import RawProxy

'''constants'''

satoshiInBitcoin = 100000000

'''length in number of hex symbols (bytes*2) of fields in raw transaction'''
versionNoLen = 4*2
varIntMin = 1*2
sequenceNoLen = 4*2
txidLen = 32*2
txIndexLen = 4*2
seqLen = 4*2
amountLen = 8*2

'''global Vars'''
witFlagPresent = False

class inTx:
	def __init__(self, txid, index, scriptLen, script, seqNo):
		self.txid = txid
		self.index = index
		self.scriptLen = scriptLen
		self.script = script
		self.sequenceNo = seqNo
	def show(self):
		print("{")
		print("\ttxid: "+ str(self.txid))
		print("\tvout: "+ str(self.index))
		print("\tscriptSig (hex): "+ self.script)
		print("\tsequence: "+ str(self.sequenceNo))
		print("}")

class outTx:
	def __init__(self, amount, scriptLen, script):
		self.amount = amount
		self.scriptLen = scriptLen
		self.script = script
	def show(self):
		print("{")
		print("\tvalue: "+ str(self.amount/satoshiInBitcoin))
		print("\tscriptPubKey (hex): "+ self.script)
		print("}")


'''Takes in little/big endian hex and returns big/little Endian Hex'''
def reverseEndian(origionalEndHex):
	if(len(origionalEndHex)%2==0):
		byteIndex = int(len(origionalEndHex)/2)-1;
		splitIn2 = [origionalEndHex[i:i+2] for i in range(0, len(origionalEndHex), 2)]
		reverse = [splitIn2[byteIndex-i] for i in range(0, byteIndex+1)]
		return ''.join(reverse)
	else:
		print("hex string not multiple of 2")
	
def calcVarLen(rawtxid):
	
	code = rawtxid[0:varIntMin]; rawtxid = rawtxid[varIntMin:]

	if(code=="fd"):
		length = 2
	elif(code=="fe"):
		length = 4
	elif(code == "ff"):
		length = 8
	else:
		length = 1

	#convert from bytes to number of hex characters
	length = length*2

	if(length==2):
		count = int(code, 16)
	else:
		count = int(reverseEndian(rawtxid[0:length]), 16); rawtxid = rawtxid[length:]

	return count, rawtxid




def extractInfo(rawtxid):
	'''versionNum(4 bytes)|optionalFlag(if present it is '0001' and indicates witness data)
		|inCount(1-9 bytes)|listofInputs|outCount(1-9 bytes)|listOfOutputs|witnesses(var(see segwit))|locktime(4 bytes)'''
	global witFlagPresent

	'''Get version num and check for optional flag indicating witness data'''
	versionNo = int(reverseEndian(rawtxid[0:versionNoLen]), 16); rawtxid = rawtxid[versionNoLen:]

	witnessflag = rawtxid[0:4]
	if(witnessflag == '0001'):
		witFlagPresent = True
		rawtxid = rawtxid[4:]
	
	''' extract inputs'''
	inputCount, rawtxid = calcVarLen(rawtxid)
	
	inputTxArray = []
	
	for i in range(0, inputCount):
		in_id = reverseEndian(rawtxid[0:txidLen]); rawtxid = rawtxid[txidLen:]
		in_index = int(reverseEndian(rawtxid[0:txIndexLen]), 16); rawtxid = rawtxid[txIndexLen:]
		in_scriptLen, rawtxid = calcVarLen(rawtxid); in_scriptLen = in_scriptLen*2
		in_script = rawtxid[0:in_scriptLen]; rawtxid = rawtxid[in_scriptLen:]
		in_seqNum = int(reverseEndian(rawtxid[0:seqLen]),16); rawtxid = rawtxid[seqLen:]
		inputObj = inTx(in_id, in_index, in_scriptLen, in_script, in_seqNum)
		inputTxArray.append(inputObj)
	
	''' extract outputs'''
	outputCount, rawtxid = calcVarLen(rawtxid)
	outputTxArray = []

	for i in range(0, outputCount):
		out_amount = int(reverseEndian(rawtxid[0:amountLen]), 16); rawtxid = rawtxid[amountLen:]
		out_scriptLen, rawtxid = calcVarLen(rawtxid); out_scriptLen = out_scriptLen*2
		out_script = rawtxid[0:out_scriptLen]; rawtxid = rawtxid[out_scriptLen:]
		OutObj = outTx(out_amount, out_scriptLen, out_script)
		outputTxArray.append(OutObj)

	return inputTxArray, outputTxArray

def show(vinArray, voutArray):
	print("---------Inputs------------");
	for i in range(0, len(vinArray)):
		vinArray[i].show()
	print("---------Outputs-----------");
	for i in range(0, len(voutArray)):
		voutArray[i].show()


def calcFees(vin, vout):
	outputs = 0;
	inputs = 0;

	#total output
	for i in range(0, len(vout)):
		outputs+=getattr(vout[i], 'amount')

	#total input	
	for i in range(0, len(vin)):
		txid = getattr(vin[i], 'txid')
		rawtxid = p.getrawtransaction(txid)
		in_vin, in_vout = extractInfo(rawtxid)
		inputs+=getattr(in_vout[getattr(vin[i], 'index')], 'amount')

	return inputs-outputs


if __name__ == '__main__':

	#connect to bitcoin-cli
	p = RawProxy(service_port=18332)

	#get transaction ID from command line
	txid = sys.argv[1]
	rawtxid = p.getrawtransaction(txid)

	#Extract info for main transaction
	vin, vout = extractInfo(rawtxid)
	fees = calcFees(vin, vout)/satoshiInBitcoin

	'''Print all info'''
	print("================================Transaction Info===================================")
	print("Num Inputs: "+ str(len(vin)))
	print("Num Outputs: "+ str(len(vout)))
	print("Fees: "+str(fees)+" BTC")
	print("Witness Info: "+ str(witFlagPresent))
	show(vin, vout);
	print("===================================================================================")











