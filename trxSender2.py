from web3 import Web3
from solcx import compile_source
import os
import datetime
# Solidity source code
with open("sav.sol", "r") as f:
    contract_source_code = f.read()
# Compile the contract
compiled_sol = compile_source(contract_source_code, output_values=["abi", "bin"])

# Retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# Get bytecode / bin
bytecode = contract_interface["bin"]

# Get ABI
abi = contract_interface["abi"]

# Web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Set pre-funded account as sender
private_key = "0xee90d6c717b00447a9b6f4d3812ee4be3e99599905fa4d79bbfac1712faef186"
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

# Check if contract has already been deployed
contract_address_file = "contract_address.txt"
if os.path.isfile(contract_address_file):
    with open(contract_address_file, "r") as f:
        contract_address = f.read().strip()
    if w3.isAddress(contract_address):
        student_management = w3.eth.contract(
            address=contract_address,
            abi=abi
        )
    else:
        print(f"Invalid contract address in {contract_address_file}, deploying new contract...")
        contract_address = None
else:
    contract_address = None

if not contract_address:
    student_management = w3.eth.contract(abi=abi, bytecode=bytecode)
    txn_dict = student_management.constructor().buildTransaction({
        'gas': 1000000, # Set maximum gas amount for the transaction
        'gasPrice': w3.toWei('10', 'gwei'), # Set gas price (in gwei) for the transaction
        'from': account.address, # Set the transaction sender
        'nonce': w3.eth.get_transaction_count(account.address), # Set the nonce
    })
    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # Save contract address to file
    with open(contract_address_file, "w") as f:
        f.write(tx_receipt.contractAddress)
    # Instantiate the contract at the deployed address
    student_management = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )

# Interact with the contract using its functions
def add_achievement(description, addr):
    txn_dict = student_management.functions.addAchievement(description, addr).buildTransaction({
        'gas': 1000000, # Set maximum gas amount for the transaction
        'gasPrice': w3.toWei('10', 'gwei'), # Set gas price (in gwei) for the transaction
        'from': account.address, # Set the transaction sender
        'nonce': w3.eth.get_transaction_count(account.address), # Set the nonce
    })
    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)

def view_function(addr):
    student = student_management.functions.getAchievements(addr).call()
    return student

# def changeDateFormat(student):
#     date_time = datetime.datetime.fromtimestamp(student)
#     return date_time
# Print the new wallet address and private key
print('New wallet address:', account.address)
print('Private key:', private_key)

#


# Example usage
add_achievement('Python Workshop', account.address)
print(view_function(account.address))
