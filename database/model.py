class voter:
    def __init__(self, name, email, electionId):
        self.username = name
        self.email = email
        self.electionId = electionId
class candidate:
    def __init__(self, name, email, electionId):
        self.username = name
        self.email = email
        self.electionId = electionId
class admin:
    def __init__(self, name, email, pwd,orgname,role,field):
        self.username = name
        self.email = email
        self.passwd = pwd
        self.orgname = orgname
        self.roleOfadmin = role
        self.field = field
class election:
    def __init__(self, electionId,adminName,postion,startDate,endDate):
        self.adminName=adminName
        self.electionId=electionId
        self.postion=postion
        self.startDate=startDate
        self.endDate=endDate
