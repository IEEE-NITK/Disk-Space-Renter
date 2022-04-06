// SPDX-License-Identifier: MIT

pragma solidity >= 0.5.0 < 0.9.0;

struct Request {
    uint space;
    uint duplications;
    uint duration;
    string[] cids;
    uint startTime;
    address[] providersList;
}

struct Provide {
    uint space;
}

// duration 
// access data 

contract DiskSpaceRenter {

    modifier afterCompletion(address r) {
        uint deadline = requesterList[r].startTime + requesterList[r].duration;
        require(block.timestamp > deadline);
        _;
    }


    address[] public requesters;
    address[] public providers;
    mapping (address => Request) public requesterList;
    mapping (address => Provide) public providerList;

    // one provider can have multiple requesters
    mapping (address => address[]) public providerToRequester;

    // one requester can have multiple providers
    mapping (address => address[]) public requesterToProvider;

    //address to amount paid  by requester and deposited to the contract account and not released to the provider account yet
    mapping (address => uint) public requesterFunds;
    
    modifier onlyRequester {
        bool flag = false;
        for(uint i=0; i<requesters.length; i++) {
            if(msg.sender == requesters[i]) flag = true;
        }
        require(flag == true);
        _;
    }

    function toBytes(address a) public pure returns (bytes memory) {
        return abi.encodePacked(a);
    }

    function sayHello() public pure returns (string memory) {
        return 'Hello World!';
    }

    modifier onlyProvider {
        bool flag = false;
        for(uint i=0; i<providers.length; i++) {
            if(msg.sender == providers[i]) flag = true;
        }
        require(flag == true);
        _;
    }


    function addRequester() public returns( bool added){
        address requester = msg.sender;
        bool flag = true;
        for(uint i=0; i<requesters.length; i++) {
            if(requesters[i] == requester) flag = false;
        }
        for(uint i=0; i<providers.length; i++) {
            if(providers[i] == requester) flag = false;
        }
        if(flag){ requesters.push(msg.sender);
        return true;}
        return false;
    }

    function addProvider(uint _spaceInMB) public returns( bool added){
        address pro = msg.sender;
        bool flag = true;
        for(uint i=0; i<requesters.length; i++) {
            if(requesters[i] == pro) flag = false;
        }
        for(uint i=0; i<providers.length; i++) {
            if(providers[i] == pro) flag = false;
        }
        if(flag) {
            providers.push(msg.sender);

            Provide memory p = Provide(_spaceInMB);
            providerList[msg.sender] = p;
            return true;
        }
        return false;
    }
    function getRequesters()public view returns( address[] memory){
        return requesters;
    }

    function getProviders()public view returns(address[] memory){
        return providers;
    }

    function getCurrentUser()public view returns( address  user){
        return msg.sender;
    }

    function currentUserTransaction()public view returns(Request memory r){
        return requesterList[msg.sender];
    }

    function addCIDToTransaction(string memory cid) public{
        requesterList[msg.sender].cids.push(cid);
    }
    
    // front end should give array of cids as argument to this func
    function requestSpace(uint _spaceInMB, uint _duplications, uint _duration, string[] memory _cids,uint startTime, address[] memory gettingProvider) public payable onlyRequester {
        // duration in seconds
        // price is a function of requesters space, duration and duplications
        // uint price = 2000000000000000000;
        // msg.value = price;
        require(msg.sender.balance > msg.value);
        
        Request memory r = Request(_spaceInMB, _duplications, _duration, _cids, startTime, gettingProvider);
        requesterList[msg.sender] = r;
        payRent();

        // keeping track of amount deposited to contract account by each requester
        requesterFunds[msg.sender] = msg.value;

        // withdraw money from requesters account
        // put it into contarcts account
        // release into provider after durtion is complete

        // transfer is from contract to any other payable address
        // payable(address(this)).transfer(msg.value);       
    }

    function payRent() payable public {
        //learn how to hide this function
    }

    function approveRequest (uint requester_index) public onlyProvider {
        address caller = msg.sender;
        address requester = requesters[requester_index];
        if(providerList[caller].space != 0) {
            if(requesterList[requester].space < providerList[caller].space) {
                if(requesterToProvider[requester].length < requesterList[requester].duplications) {
                    providerToRequester[caller].push(requester);
                    requesterToProvider[requester].push(caller);

                    providerList[caller].space -= requesterList[requester].space;

                    requesterList[requester].startTime = block.timestamp;
                    requesterList[requester].providersList.push(caller);
                }

                else {
                    // already y providers exist
                }
            }
            else {
                // space insufficient
            }
        }
        else {
            // not a provider
        }
    }

    // releasePayment() is called by provider. it checks the duration and transfers the funds
    // argument is requesters address
    function releasePayment (address r) public afterCompletion(r) onlyProvider {
        require(providerToRequester[msg.sender].length != 0);
        uint amount = requesterFunds[r]/requesterList[r].duplications;
        payable(msg.sender).transfer(amount);
        updateMappings(r, msg.sender);
    }

    function updateMappings(address r, address p) private {
        // in requester, remove provider
        address[] memory providerArray = requesterToProvider[r];
        
        uint index;
        for(index=0; index<providerArray.length; index++) {
            if(requesterToProvider[r][index] == p) {
                break;
            }
        }
        for(uint j = index; j < providerArray.length-1; j++) {
            requesterToProvider[r][j] = requesterToProvider[r][j+1];
        }
        delete requesterToProvider[r][requesterToProvider[r].length-1];


        // in provider remove requester
        address[] memory requesterArray = providerToRequester[p];
        
        uint ind;
        for(ind=0; ind<requesterArray.length; ind++) {
            if(providerToRequester[p][ind] == r) {
                break;
            }
        }
        for(uint j = ind; j <requesterArray.length-1; j++) {
            providerToRequester[p][j] = providerToRequester[p][j+1];
        }
        delete providerToRequester[p][requesterToProvider[p].length-1];
    }
    uint[] public space;
    uint[] public duplicationss;
    uint[] public duration;
    uint[] public sstartTime;
    address[] public requestersOfTransactions;
    uint[] public indexes;
    function getAllTransactions() public returns(uint[] memory,uint[] memory , uint[] memory, uint[] memory, address[] memory, uint[] memory) {
        for(uint i = 0;i<requesters.length;i++){
            if(requesterList[requesters[i]].startTime!=0){
                requestersOfTransactions.push(requesters[i]);
                space.push(requesterList[requesters[i]].space);
                duplicationss.push(requesterList[requesters[i]].duplications);
                sstartTime.push(requesterList[requesters[i]].startTime);
                duration.push(requesterList[requesters[i]].duration);
                indexes.push(i);
            }
        }
        return (space,duplicationss,duration,sstartTime,requestersOfTransactions,indexes);
    }
}
