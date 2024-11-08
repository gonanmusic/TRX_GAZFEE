import time
from tronpy import Tron
from tronpy.keys import PrivateKey

# Setup the Tron client on a specific network if needed (e.g., "nile" for testnet, "mainnet" for the main network)
client = Tron(network="nile")  # Use "mainnet" for the live network or "nile" for the test network

# Wallets Details
sender_private_key = "PRIVATE KEY"  # Replace with the private key of the sender's address.
sender_address = "SENDER ADRESS"  # Replace with the TRX address of the sender.
receiver_address = "YOUR ADRESS"  # Replace with your own adress

# Initialize the previous balance
previous_balance = client.get_account(sender_address)['balance']

def check_for_new_deposit():
    global previous_balance
    current_balance = client.get_account(sender_address)['balance']
    
    if current_balance > previous_balance:
        new_deposit_amount = current_balance - previous_balance
        previous_balance = current_balance
        print(f"Nouveau dépôt détecté : {new_deposit_amount} TRX")
        transfer_trx(new_deposit_amount)

def transfer_trx(amount):
    txn = (
        client.trx.transfer(sender_address, receiver_address, amount)
        .build()
        .sign(PrivateKey(bytes.fromhex(sender_private_key)))
    )
    txn_hash = txn.broadcast().wait()
    print(f"Transfert terminé. Hash de la transaction : {txn_hash}")

while True:
    check_for_new_deposit()
    time.sleep(10)  # Check every 10 seconds
