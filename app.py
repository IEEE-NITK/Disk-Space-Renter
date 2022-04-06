import json
from web3 import Web3, HTTPProvider
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import ipfshttpclient
import requests


blockchain_address = 'http://127.0.0.1:9545'

web3 = Web3(HTTPProvider(blockchain_address))

web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = 'build/contracts/DiskSpaceRenter.json'

deployed_contract_address = '0x828b0b9D475C12AB15939DFCe8e6368E489B33AA'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is not persisted to the blockchain)
print("Welcome to the Disk Space Renter System!")
prev_user = int(input("If you are an old user, enter 1, else 2 : "))
print(prev_user)
isRequester = False
if(prev_user==1):
    print("Old User")
    
else:
    print("New User")
    isRequester = int(input("Are you a requester?(Press 1 if yes!)"))
    if(isRequester==1):
        isRequester=True
        added = contract.functions.addRequester().transact()
        if(added):print("Registered as a Requester")
        else:print("Could not register!")
    else:
        isRequester=False
        spaceMBProvider = int(input("Kindly input the amount of data you can provide : "))
        added = contract.functions.addProvider(spaceMBProvider).transact()
        if(added):print("Registered as a Provider")
        else:print("Could not register!")

current_user = contract.functions.getCurrentUser().call()
print("Your ID is ",current_user)

print("Here is the list of all requesters")
answer = contract.functions.getRequesters().call()
print(answer)
print("Here is the list of all providers")
answer1 = contract.functions.getProviders().call()
print(answer1)

if(isRequester):
    currentUserTransaction = contract.functions.currentUserTransaction().call()
    if currentUserTransaction[-2]==0:
        print("\n\nYOU DON'T HAVE ANY TRANSACTIONS CURRENTLY!\n\n")
        wantToReqSpace = int(input("Want to request space? : "))
        if(wantToReqSpace==1):
            print("Request Space Dashboard")
            contract.functions.requestSpace(200,2,50000,[],1,[]).transact()
            print("Transaction Created!")
        else:
            print("Okay, thank you!")
    else:
        print("\n\nYOU HAVE THE FOLLOWING TRANSACTION\n\n")
        print("Space : ",currentUserTransaction[0])
        print("Duplications : ",currentUserTransaction[1])
        print("Duration : ",currentUserTransaction[2])
        print("CIDs : ",currentUserTransaction[3])
        print("Start Time : ",currentUserTransaction[4])
        print('\n\n')

        wantToUploadFile = int(input("Do you want to upload a file? : "))
        if(wantToUploadFile==1):
            cid = "QmYFQKAWgf9shjNm5CetXz2r1vJ5FHd1FXaWh4votXNSN4"
            contract.functions.addCIDToTransaction(cid).transact()
            print("FILE UPLOADED")
    print('Here are the requesters!')    
    ans = contract.functions.getAllTransactions().call()
    print(ans)      


if(isRequester!=True):
    print("Here are the requesters' transactions!")    
    print("Space\tDuplications\tDuration\tStart Time\tRequester")
    ans = contract.functions.getAllTransactions().call()
    print(ans)
    wantToProvideForWhichRequester = int(input("Want to provide for which transaction? : "))  
    #wtf is happening here
    if(wantToProvideForWhichRequester!=0):
        addressToProvideFor = ans[5][wantToProvideForWhichRequester-1]
        print(addressToProvideFor)
        contract.functions.approveRequest(addressToProvideFor).transact()
        print("You are now part of this transaction!")