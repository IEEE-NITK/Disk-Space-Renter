# Disk-Space-Renter

## Mentors

- Ikjot Dhody
- Chaitanya Shyam

## Members

- Tejas Sankpal
- Advaith Prasad Curpod
- Anurag Kumar

## Aim

- Create a decentralized file sharing platform where users (disk space requesters & disk space providers) come together to leverage the benefits of blockchain & trustless decentralization.
- Build an incentive layer on top of IPFS enabling disk space providers to agree to store files of disk space requesters in return for a small fee.
- Create a CLI application to implement the same. 

## Introduction

Disk space renter is an application bridging the gap between a decentralized file sharing protocol and a users requirement for a cloud service to store his files remotely, by incentivising the process of file storage and retrieval. The user (requester) who wants to use the service will have to pay (in ETH) to all the providers who are hosting his content. The amount is directly proportional to the duration of storage and file size.

## Design and Tech Stack

- The codebase has 3 parts, CLI Frontend, Intermediate connector connecting Python, IPFS & Ethereum, and Backend which includes the Ethereum Smart Contract written in Solidity. Smart contracts cover the business logic of the application, providing functionalities like space request for the requesters, a list of providers providing for each requester etc.

- The Web3 library in python is used to connect the front end code and the smart contract. Smart contracts expose their public address and ABI (Abstract Binary Interface) which acts as an interface/API for the front end code.

- IPFS (Interplanetary File Sharing), a content based file sharing protocol works under the hood when a requester requests for space and a provider approves the request. The protocol takes care of secure one-way hashing, easy retrieval of files using the CID.

- The project is built on Truffle suite which provides a development environment and a personal blockchain to test and deploy contracts in an EVM like environment.
