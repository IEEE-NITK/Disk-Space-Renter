class transaction:
    def __init__(self, space,duplications,duration,cids,startTime,providers,requestersOfTransactions,index):
        self.space = space
        self.duplications = duplications
        self.duration = duration
        self.startTime = startTime
        self.requestersOfTransactions = requestersOfTransactions
        self.index = index
        self.cids = cids
        self.providers = providers
        self.canProvide = (len(providers)<duplications)
    def printTransaction(self):
        print("Space : ",self.space)
        print("Duplications : ",self.duplications)
        print("Duration : ",self.duration)
        print("CIDs : ",self.cids)
        print("Start Time : ",self.startTime)
        print("Providers allotted : ",self.providers)
        print("Requester account : ",self.requestersOfTransactions)