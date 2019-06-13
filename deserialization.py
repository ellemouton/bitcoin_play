
satoshiInBitcoin = 100000000

'''length in number of hex symbols (bytes*2) of fields in raw transaction'''
versionNoLen = 4*2
flagLen = 1*2
sequenceNoLen = 4*2
txidLen = 32*2
txIndexLen = 4*2
scriptLenLen = 1*2 # NOTE this could vary between 1-9 bytes.
seqLen = 4*2
amountLen = 8*2

txid =  '0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2'
#getrawtransaction(txid): 0100000001186f9f998a5aa6f048e51dd8419a14d8a0f1a8a2836dd734d2804fe65fa35779000000008b483045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e381301410484ecc0d46f1918b30928fa0e4ed99f16a0fb4fde0735e7ade8416ab9fe423cc5412336376789d172787ec3457eee41c04f4938de5cc17b4a10fa336a8d752adfffffffff0260e31600000000001976a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788acd0ef8000000000001976a9147f9b1a7fb68d60c536c2fd8aeaa53a8f3cc025a888ac00000000
rawtxid  = '0100000001186f9f998a5aa6f048e51dd8419a14d8a0f1a8a2836dd734d2804fe65fa35779000000008b483045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e381301410484ecc0d46f1918b30928fa0e4ed99f16a0fb4fde0735e7ade8416ab9fe423cc5412336376789d172787ec3457eee41c04f4938de5cc17b4a10fa336a8d752adfffffffff0260e31600000000001976a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788acd0ef8000000000001976a9147f9b1a7fb68d60c536c2fd8aeaa53a8f3cc025a888ac00000000'


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
	
def extractInfo(rawtxid):
	versionNo = int(reverseEndian(rawtxid[0:versionNoLen]), 16); rawtxid = rawtxid[versionNoLen:]

	''' extract inputs'''
	inputCount = int(reverseEndian(rawtxid[0:flagLen]), 16); rawtxid = rawtxid[flagLen:]

	inputTxArray = []

	for i in range(0, inputCount):
		in_id = reverseEndian(rawtxid[0:txidLen]); rawtxid = rawtxid[txidLen:]
		in_index = int(reverseEndian(rawtxid[0:txIndexLen]), 16); rawtxid = rawtxid[txIndexLen:]
		in_scriptLen = int(reverseEndian(rawtxid[0:scriptLenLen]), 16)*2; rawtxid = rawtxid[scriptLenLen:]
		in_script = rawtxid[0:in_scriptLen]; rawtxid = rawtxid[in_scriptLen:]
		in_seqNum = int(reverseEndian(rawtxid[0:seqLen]),16); rawtxid = rawtxid[seqLen:]
		inputObj = inTx(in_id, in_index, in_scriptLen, in_script, in_seqNum)
		inputTxArray.append(inputObj)

	''' extract outputs'''
	outputCount = int(reverseEndian(rawtxid[0:flagLen]), 16); rawtxid = rawtxid[flagLen:]

	outputTxArray = []

	for i in range(0, outputCount):
		out_amount = int(reverseEndian(rawtxid[0:amountLen]), 16); rawtxid = rawtxid[amountLen:]
		out_scriptLen = int(reverseEndian(rawtxid[0:scriptLenLen]), 16)*2; rawtxid = rawtxid[scriptLenLen:]
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
	#for i in range(0, len(vin)):
		#get txid
		#get rawtxid
		#in_vin, in_vout = extractInfo(rawindexid)
		#inputs+=getattr(in_vout[getattr(vin[i], 'index')], 'amount')

	rawtx = '0100000001524d288f25cada331c298e21995ad070e1d1a0793e818f2f7cfb5f6122ef3e71000000008c493046022100a59e516883459706ac2e6ed6a97ef9788942d3c96a0108f2699fa48d9a5725d1022100f9bb4434943e87901c0c96b5f3af4e7ba7b83e12c69b1edbfe6965f933fcd17d014104e5a0b4de6c09bd9d3f730ce56ff42657da3a7ec4798c0ace2459fb007236bc3249f70170509ed663da0300023a5de700998bfec49d4da4c66288a58374626c8dffffffff0180969800000000001976a9147f9b1a7fb68d60c536c2fd8aeaa53a8f3cc025a888ac00000000'
	in_vin, in_vout = extractInfo(rawtx)
	inputs+=getattr(in_vout[getattr(vin[0], 'index')], 'amount')

	return inputs-outputs

#Extract and show info for main transaction
vin, vout = extractInfo(rawtxid)
show(vin, vout);

#Calculate fees
print("Fees: "+str(calcFees(vin, vout)/satoshiInBitcoin)+" BTC")









