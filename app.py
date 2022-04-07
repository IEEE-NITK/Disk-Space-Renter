import json
import tkinter
from web3 import Web3, HTTPProvider
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import ipfshttpclient
import ipfsApi
import requests

from contracts.transaction import transaction


blockchain_address = 'http://127.0.0.1:9545'

web3 = Web3(HTTPProvider(blockchain_address))

web3.eth.defaultAccount = web3.eth.accounts[0]

globalAccountList = web3.eth.accounts

compiled_contract_path = 'build/contracts/DiskSpaceRenter.json'

deployed_contract_address = '0x828b0b9D475C12AB15939DFCe8e6368E489B33AA'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

globalProviderList = contract.functions.getProviders().call()
globalRequesterList = contract.functions.getRequesters().call()
globalTransactionList = contract.functions.getAllTransactions().call()
globalTransactionDict = {}

def getProviderSpace(sender):
    return contract.functions.getProviderSpace(sender).call()

# Parse all transactions
# Get number of transactions
def getUserTransaction(sender):
    return contract.functions.getUserTransaction(sender).call()        
totalNumberOfTransactions = len(globalTransactionList[0])
for i in range(0,totalNumberOfTransactions):
    tempCurrTransaction = getUserTransaction(globalTransactionList[4][i])
    globalTransactionDict[globalTransactionList[4][i]] = transaction(tempCurrTransaction[0],tempCurrTransaction[1],tempCurrTransaction[2],tempCurrTransaction[3],tempCurrTransaction[4],tempCurrTransaction[5],globalTransactionList[4][i],globalTransactionList[-1][i]) 
      
def refreshTransactions():
    globalTransactionList = contract.functions.getAllTransactions().call()
    totalNumberOfTransactions = len(globalTransactionList[0])
    globalTransactionDict = {}
    for i in range(0,totalNumberOfTransactions):
        tempCurrTransaction = getUserTransaction(globalTransactionList[4][i])
        globalTransactionDict[globalTransactionList[4][i]] = transaction(tempCurrTransaction[0],tempCurrTransaction[1],tempCurrTransaction[2],tempCurrTransaction[3],tempCurrTransaction[4],tempCurrTransaction[5],globalTransactionList[4][i],globalTransactionList[-1][i]) 
    

from art import *
tprint("Disk Space Renter System")


prev_user = int(input("If you are an old user, enter 1, else 2 : "))
isRequester = False
accountAddress = ""

if(prev_user==1):
    # Old User
    accountAddress = input("Please enter your account address : ")
    # check if he is old requester
    for requester in globalRequesterList:
        if(requester == accountAddress):
            print("Welcome Back, you are an old requester!")
            web3.eth.defaultAccount = accountAddress
            isRequester= True
    # check if he is old provider
    for provider in globalProviderList:
        if(provider == accountAddress):
            print("Welcome Back, you are an old provider!")
            web3.eth.defaultAccount = accountAddress
            isRequester= False

else:
    # New User

    # Look for an available address
    for account in globalAccountList:
        availableAddress = True
        for requester in globalRequesterList:
            if(requester == account):
                availableAddress = False
        for provider in globalProviderList:
            if(provider == account):
                availableAddress = False
        if(availableAddress):
            accountAddress = account      
            web3.eth.defaultAccount = accountAddress
            break  
        

    isRequester = int(input("Are you a requester?(Press 1 if yes!) : "))

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
print("\nYour ID is ",current_user,'\n')

print("\nHere is the list of all requesters")
answer = contract.functions.getRequesters().call()
print(answer,'\n')
print("\nHere is the list of all providers")
answer1 = contract.functions.getProviders().call()
print(answer1,'\n')

if(isRequester):
    currentUserTransaction = contract.functions.currentUserTransaction().call()
    if currentUserTransaction[-2]==0:
        print("\n\nYOU DON'T HAVE ANY TRANSACTIONS CURRENTLY!\n\n")
        wantToReqSpace = int(input("Want to request space? : "))
        if(wantToReqSpace==1):
            print("Request Space Dashboard")
            space = int(input("Kindly input the space you require : "))
            duplications = int(input("Kindly input the number of duplications you desire : "))
            duration = int(input("Kindly input the duration of the space you need : "))
            contract.functions.requestSpace(space,duplications,duration,[],[]).transact()
            print("Transaction Created!")
        else:
            print("Okay, thank you!")
    else:
        print("\n\nYOU HAVE THE FOLLOWING TRANSACTION\n\n")
        globalTransactionDict[accountAddress].printTransaction()

        wantToUploadFile = int(input("Do you want to upload a file? : "))
        if(wantToUploadFile==1):
            api = ipfsApi.Client('127.0.0.1', 5001)
            filename = askopenfilename()
            res = api.add(filename)
            cid = res[0]["Hash"]
            print("FILE UPLOADED")
            print("Here is the CID of the file that was uploaded to IPFS : ",cid)
            contract.functions.addCIDToTransaction(cid).transact()
            


if(isRequester!=True):
    # This is a provider
    
    #check if user is providing
    requesterBeingProvided = contract.functions.getTransactionOfProvider().call()
    if(requesterBeingProvided==accountAddress):
        print("You are currently not part of any transaction!")
        print("Here are the requesters' transactions!\n")    
        for i, (k, v) in enumerate(globalTransactionDict.items()):
            if(v.canProvide and getProviderSpace(accountAddress)>=v.space):
                print("Transaction ",i+1,'\n')
                v.printTransaction()
                print('\n')
        wantToProvideForWhichRequester = (input("Want to provide for which account?(enter 0 for none) : "))  
        if(wantToProvideForWhichRequester!="0"):
            added = contract.functions.approveRequest(wantToProvideForWhichRequester).transact()
            if(added):print("You are now part of this transaction!")
            else: print("You were not added to transaction due to some inconsistency!")
    else:
        print("You are currently providing for the following transaction\n")
        transactionProvidingFor = globalTransactionDict[requesterBeingProvided]
        transactionProvidingFor.printTransaction()    
        print('\n')
    



