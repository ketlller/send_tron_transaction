from web3 import Web3

# Initialize endpoint URL
node_url = "https://polygon-mumbai.g.alchemy.com/v2/51BnvyCYzbJkcMV8Tum46uelyx2jsFJT"

# Create the node connection
web3 = Web3(Web3.HTTPProvider(node_url))

if web3.isConnected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")

# Initialize the address calling the functions/signing transactions
caller = "0xA3A6778D64FA74FF962a123936C1D7c5FD4591d4"
private_key = "0xca7fc97a3322996e02ec7b8e079f85c56c038d627ba617128f34ce0d87144dc4"  # To sign the transaction

# Initialize address nonce
nonce = web3.eth.getTransactionCount(caller)

# Initialize contract ABI and address
abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "certificateHash",
				"type": "string"
			}
		],
		"name": "remove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "certificateHash",
				"type": "string"
			}
		],
		"name": "set",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string[]",
				"name": "bulkHash",
				"type": "string[]"
			}
		],
		"name": "setBulk",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "certificateHash",
				"type": "string"
			}
		],
		"name": "get",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "myMap",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
contract_address = "0x611af2bf18a70a058046a261d5d2ab5d7300cc2b"
contract_address = web3.toChecksumAddress(contract_address)

# Create smart contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# initialize the chain id, we need it to build the transaction for replay protection
chain_id = web3.eth.chainId

# Call the `set` function
function_inputs = "123456789bbbb"

# Build the transaction
txn = contract.functions.set(function_inputs).buildTransaction(
    {
        "chainId": chain_id,
        "gas": 1000000,
        "gasPrice": web3.toWei("10", "gwei"),
        "nonce": nonce,
    }
)

# Sign the transaction
signed_txn = web3.eth.account.signTransaction(txn, private_key)

# Send the transaction
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
receipt = web3.eth.waitForTransactionReceipt(txn_hash)

# Print the transaction receipt
print(receipt)






# Call the get function to retrieve the values from the contract
getValues = contract.functions.get("babu1234#@").call()
print(getValues)

# tx_hash = contract.functions.set('123456789bbbb').transact()
# web3.eth.waitForTransactionReceipt(tx_hash)

print("Updated Value:" )
getValues = contract.functions.get("123456789bbbb").call()
print(getValues)
