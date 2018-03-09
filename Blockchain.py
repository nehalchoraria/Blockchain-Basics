# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 15:44:41 2018

@author: Nehal
"""
import hashlib
import time
import random

class Block:
    
    previousHash = ""
    blockData = []
    blockHash = ""
    noOfTransactions = 0
    height = 0
    size = 0 #inBytes
    timestamp = time.time()
    
    def __init__(self,previousHash,height,blockData):
        self.previoushash = previousHash 
        self.blockData = blockData 
        self.timestamp = time.time()
        
        allTransactions = [ transactionInfo for transaction in blockData for transactionInfo in transaction ]
        allTransactions = " ".join(str ( allTransactions ) )
        
        self.noOfTransactions = len ( [ transaction for transaction in blockData ] )
        self.size = len(allTransactions.encode("utf8"))
        self.height = height
        self.previousHash = previousHash
        
        blockHash = hashlib.sha256( previousHash.encode() +  allTransactions.encode()).hexdigest()
        self.blockHash = blockHash
        
    
    def getBlockSummary(self):
        if self.height == 0:
            previousBlock = "-"
        else:
            previousBlock = self.height - 1
            
        return { "noOfTransactions":self.noOfTransactions,
                "height":self.height,
                "timestamp":self.timestamp,
                "previousHash":self.previousHash,
                "blockHash":self.blockHash,
                "previousBlock":previousBlock,
                "size": self.size,
                "blockdata": self.blockData,
                }
    
genesisblock = Block("Random Hardcoded Hash Value",0,[["Transaction1","Timestamp","Size"],["Transaction2"]])
lastBlockCreated = 0
allBlockList = [genesisblock]

def blockChainSummary(allBlockList,counter=0):
    print("".center(70,"*"))
    for blocks in allBlockList:
        if counter == 0:
            print("Genesis Block".center(50,"-"))
        else:
            print( ("Block "+str(counter)).center(50,"-"))
        counter = counter + 1
        
        for x,y in (blocks.getBlockSummary()).items():
            if isinstance(y,list):
                for transactionsInBlock in y:
                    for eachTransactionDetail in transactionsInBlock:
                        print("    "+eachTransactionDetail)
            else:
                print(x,":",y)
        print("\n")
    print("".center(70,"*"))
    
def findTransaction(allBlockList,transactionSearch):
    
    foundCheck = False
    
    AllblockTransactions = [ [x,y] for blocks in allBlockList 
            for x,y in (blocks.getBlockSummary()).items() if isinstance(y,list) ]
#    print(AllblockTransactions)
    
    output = ""
    for transactionsInBlock in AllblockTransactions:
        for eachBlock in transactionsInBlock:
            if isinstance(eachBlock,list):
                for transaction in eachBlock:
                    for eachTransactionDetail in transaction:
                       if transactionSearch in eachTransactionDetail:
                           foundCheck = True
                       if foundCheck:
                           output = output + eachTransactionDetail + "\n"
                    if foundCheck:
                        return output
                    
    return "Transaction not found. Are you sure it is right?"
    
print("Choose the following : ")
print("1. Create new block ")
print("2. View an existing block ")
print("3. Search transaction in blockchain ")
print("4. Quit")

while True:
    
    inputValue = input("Choose from 1,2,3,4 : ")
    
    if inputValue == '1':
        print("New block being created ".center(50,"-"))
        while(True):
            print("Do you want to manually enter transaction details y/n?")
            option = input("Choose from y,n (n = Generates Random Transaction) : ")
            Transactions = []
            if option == "y":
                try:
                    noOfTransactions = input("Enter number for transactions : ") 
                    noOfTransactions = int ( noOfTransactions )
                except:
                    print("Incorrect Value. Please try again.")
                else:
                    for i in range(noOfTransactions):
                        try:
                            amount = int ( input("Enter amount for transaction : ") )
                            transactionAddress = random.getrandbits(128)
                            fromAddress = random.getrandbits(64)
                            toAddress = random.getrandbits(64)
                            Transactions.append(["Transaction Address : "+str(transactionAddress),
                                                 "From Address : "+str(fromAddress),
                                                 "To Address : "+str(toAddress),
                                                 "Amount : "+str(amount)]) 
                        except:
                            print("Incorrect Value Found. Transaction Aborted! ")
                            
                    break
                
            else:
                for i in range( random.randint(1,10) ):
                    transactionAddress = random.getrandbits(128)
                    fromAddress = random.getrandbits(64)
                    toAddress = random.getrandbits(64)
                    amount = random.randint(1,200)
                    Transactions.append(["Transaction Address : "+str(transactionAddress),
                                         "From Address : "+str(fromAddress),
                                         "To Address : "+str(toAddress),
                                         "Amount : "+str(amount)]) 
                break
            
        newBlock = Block( (allBlockList[-1]).blockHash ,lastBlockCreated+1,Transactions)
        print("Block Created!",end="")
        lastBlockCreated = lastBlockCreated + 1
        allBlockList.append(newBlock)
            
            
    elif inputValue == '2':
        blockChainSummary(allBlockList)
    
    elif inputValue == '3':
        transactionSearch = input("Enter transaction to be searched in Blockchain : ")
        print ( findTransaction(allBlockList,transactionSearch) )
    elif inputValue == '4':
        break      
    else:
        print("Incorrect Value. Please try again.")



