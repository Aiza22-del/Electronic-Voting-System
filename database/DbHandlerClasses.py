import json
import pymysql
from  database.model import *
class DbModelOfElection:
    def __init__(self, host, u, password, database):
        self.host = host
        self.user = u
        self.password = password
        self.database = database
    def insert(self,election):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'insert into election(electionId,adminName,post,startDate,endDate)values(%s,%s,%s,%s,%s)'
            arg = (election.electionId,election.adminName,election.postion,election.startDate,election.endDate)
            mydbcursor.execute(sql,arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def removeByElectionId(self, electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql='delete from election where electionId=%s'
            arg=(electionId)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()

    def getEndDate(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select endDate from election where electionId=%s'
            arg = (electionId)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            if data !=None:
                return data[0][0]
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getCheckElectionId(self, electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from election where electionId=%s'
            arg = (electionId)
            mydbcursor.execute(sql, arg)
            data= mydbcursor.fetchall()
            for item in data:
                return True
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getAllElectionId(self,adminName):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from election where adminName=%s'
            arg=(adminName)
            mydbcursor.execute(sql,arg)
            data = mydbcursor.fetchall()
            myDic = {}
            myList = []
            for item in data:
                myDic.update(electionId=item[0])
                myList.append(myDic)
                myDic = {}
            return myList
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getAllRecords(self,adminName):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from election where adminName=%s'
            arg=(adminName)
            mydbcursor.execute(sql,arg)
            data = mydbcursor.fetchall()
            myDic = {}
            myList = []
            for item in data:
                myDic.update(electionId=item[0])
                myDic.update(post=item[2])
                if(item[3]==None):
                    myDic.update(winnerName='--(continue)--')
                else:
                    myDic.update(winnerName=item[3])
                sdate=item[4]
                edate=item[5]
                edate = edate.strftime("%Y-%m-%d")
                sdate = sdate.strftime("%Y-%m-%d")
                myDic.update(startDate=sdate)
                myDic.update(endDate=edate)
                myList.append(myDic)
                myDic = {}
            return myList
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def insertWinner(self,winnerName,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'update election set winnerName=%s where electionId=%s'
            arg=(winnerName,electionId)
            mydbcursor.execute(sql,arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getAllElectionDetailById(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from election where electionId=%s'
            arg=(electionId)
            mydbcursor.execute(sql,arg)
            data = mydbcursor.fetchall()
            myDic = {}
            myList = []
            for item in data:
                myDic.update(electionId=item[0])
                myDic.update(adminName=item[1])
                myDic.update(post=item[2])
                myDic.update(startDate=item[4])
                myDic.update(endDate=item[5])
                return myDic
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def checkValidElectionId(self, electionId,adminName):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from election where electionId=%s and adminName=%s'
            arg = (electionId,adminName)
            mydbcursor.execute(sql,arg)
            data = mydbcursor.fetchall()
            for item in data:
                return True
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
class DbModelOfAdmin:
    def __init__(self, host, u, password, database):
        self.host = host
        self.user = u
        self.password = password
        self.database = database
    def insertAdmin(self,admin):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'insert into admin(username,email,passwd,orgname,roleOfadmin,field)values(%s,%s,%s,%s,%s,%s)'
            arg = (admin.username,admin.email,admin.passwd,admin.orgname,admin.roleOfadmin,admin.field)
            mydbcursor.execute(sql,arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getElectionId(self,name):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from admin where username=%s'
            arg = (name)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            if data!=None:
                return data[0][7]
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getDataForProfilePage(self, name):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from admin where username=%s'
            arg = (name)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            myDic = {}
            for item in data:
                myDic.update(username=item[0])
                myDic.update(email=item[1])
                myDic.update(roleOfAdmin=item[4])
                myDic.update(orgname=item[3])
                myDic.update(field=item[5])

            return myDic
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def deactivateAccount(self,username):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'delete from admin where username= %s '
            arg = (username)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True
        except Exception as e:
            return str(e)
        finally:
            mydb.close()
            mydbcursor.close()
    def login(self,username,passwd):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from admin where username= %s and passwd= %s'
            arg = (username,passwd)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            if data == ():
                return False
            else:
                return True
        except Exception as e:
            return str(e)
        finally:
            mydb.close()
            mydbcursor.close()
class DbModelOfVoter:
    def __init__(self, host, u, password, database):
        self.host = host
        self.user = u
        self.password = password
        self.database = database
    def login(self,username,id):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where username= %s and voterid= %s'
            arg = (username,id)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            for item in data:
                return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getVoterId(self,email, electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select voterid from voter where email= %s and electionId= %s'
            arg = (email, electionId)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            for item in data:
                return item[0]
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def removeVoterByElectionId(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'delete from voter where electionId= %s'
            arg = (electionId)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getDataForProfilePage(self,voterid):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where voterid=%s'
            arg = (voterid)
            mydbcursor.execute(sql, arg)
            data = mydbcursor.fetchall()
            myDic = {}
            for item in data:
                myDic.update(voterid=item[0])
                myDic.update(username=item[1])
                myDic.update(email=item[2])
            return myDic
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()

    def getVote(self,id):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where voterid=%s'
            arg = (id)
            mydbcursor.execute(sql,arg)
            data=mydbcursor.fetchall()
            if data[0][3]!=None:
                return data[0][3]
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def SetVote(self, id):
        try:
            vote='Casted'
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'update voter set vote=%s where voterid=%s'
            arg = (vote,id)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getElectionId(self,id):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where voterid=%s'
            arg = (id)
            mydbcursor.execute(sql,arg)
            data=mydbcursor.fetchall()
            if data!=None:
                return data[0][4]
            else:
                return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def insert(self,voter):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'insert into voter(username,email,electionId)values(%s,%s,%s)'
            arg = (voter.username,voter.email,voter.electionId)
            mydbcursor.execute(sql,arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getAllData(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where electionId =%s'
            arg = (electionId)
            mydbcursor.execute(sql, arg)
            data=mydbcursor.fetchall()
            return data
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getVotersbyElectionid(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where electionId=%s'
            arg=(electionId)
            mydbcursor.execute(sql,arg)
            data=mydbcursor.fetchall()
            myDic = {}
            myList = []
            for item in data:
                myDic.update(voterid=item[0])
                myDic.update(username=item[1])
                myDic.update(email=item[2])
                if(item[3]==None):
                    myDic.update(vote='Pending')
                else:
                     myDic.update(vote=item[3])
                myDic.update(electionId=item[4])
                myList.append(myDic)
                myDic = {}
            return myList
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getVoterbyId(self,voterid):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from voter where voterid=%s'
            arg=(voterid)
            mydbcursor.execute(sql,arg)
            data=mydbcursor.fetchall()
            voterDic={}
            voterList=[]
            for item in data:
                voterDic.update(username=item[1])
                voterDic.update(email=item[2])
                voterDic.update(electionId=item[4])
                voterList.append(voterDic)
                voterDic = {}
            return voterList
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()

class DbModelOfCandidate:
    def __init__(self, host, u, password, database):
        self.host = host
        self.user = u
        self.password = password
        self.database = database
    def getWinner(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select username,email,max(noOfVote) from candidate where electionId=%s'
            arg=(electionId)
            mydbcursor.execute(sql,arg)
            data = mydbcursor.fetchall()
            candDic={}
            for item in data:
                candDic.update(username=item[0])
                candDic.update(email=item[1])
                if(item[2]==None):
                    candDic.update(noOfVote='0')
                else:
                    candDic.update(noOfVote=item[2])
                return candDic
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def insert(self,candidate):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'insert into candidate(username,email,electionId)values(%s,%s,%s)'
            arg = (candidate.username,candidate.email,candidate.electionId)
            mydbcursor.execute(sql,arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getCandidatebyid(self, electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor=mydb.cursor()
            sql = 'select * from candidate where electionId = %s'
            arg = (electionId)
            mydbcursor.execute(sql,arg)
            data = mydbcursor.fetchall()
            candidateDic = {}
            candidateList = []
            for item in data:
                candidateDic.update(candidateId=item[0])
                candidateDic.update(username=item[1])
                candidateDic.update(email=item[2])
                if(item[3]==None):
                    candidateDic.update(noOfVote=0)
                else:
                    candidateDic.update(noOfVote=str(item[3]))
                candidateDic.update(electionId=item[4])
                candidateList.append(candidateDic)
                candidateDic = {}
            return candidateList
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getCandidates(self):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from candidate'
            mydbcursor.execute(sql)
            data=mydbcursor.fetchall()
            return data
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def updatevote(self,Id):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql1 = 'select * from candidate where candidateid=%s'
            arg1 = (Id)
            mydbcursor.execute(sql1,arg1)
            data=mydbcursor.fetchall()
            vote=data[0][3]
            if vote==None:
                vote=1
            else:
                vote=vote+1
            sql2=' update candidate set noOfvote=%s where candidateid=%s'
            arg2=(vote,Id)
            mydbcursor.execute(sql2, arg2)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def getCheckCandidate(self):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'select * from candidate'
            mydbcursor.execute(sql)
            data= mydbcursor.fetchall()
            for item in data:
                return True
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def CheckCandidateisVoter(self,electionId,userName):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql1 = 'select username from candidate where electionId=%s and username=%s'
            arg1=(electionId,userName)
            mydbcursor.execute(sql1,arg1)
            data1= mydbcursor.fetchall()
            candidateUsername=None
            for item in data1:
                candidateUsername=item[0]
            sql2='select * from voter where electionId=%s and username=%s'
            arg2=(electionId,candidateUsername)
            mydbcursor.execute(sql2, arg2)
            data2=mydbcursor.fetchall()
            for item in data2:
                return True
            return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()
    def removeCandidateByElectionId(self,electionId):
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database)
            mydbcursor = mydb.cursor()
            sql = 'delete from candidate where electionId= %s'
            arg = (electionId)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            mydb.close()
            mydbcursor.close()


