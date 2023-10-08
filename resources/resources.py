from datetime import datetime,date
from database.DbHandlerClasses import *
from database.model import *
from flask_restful import Resource
from flask import request,render_template,Response,session,jsonify
from flask_session import Session
from email.message import EmailMessage
import ssl
import smtplib
import json
duplicateApp=None
def copyAppInstance(app):
    global duplicateApp
    duplicateApp = app
Session(duplicateApp)
def dbDictionary(app):
    app.config.from_pyfile("config.py")
    return {'host':app.config['HOST'],'user':app.config['USER'],'password':app.config['PASSWORD'],'database':app.config['DATABASE']}
class AdminSignup(Resource):
    def post(self):
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            passwd = request.form.get("passwd")
            orgname = request.form.get("orgname")
            role = request.form.get("role")
            field = request.form.get("field")
            emailCheck = email.split('@')
            if len(emailCheck) == 1:
                return Response(response=render_template('register.html', msg="Please Enter Valid syntax of Email."))
            if emailCheck[1] != "gmail.com" and emailCheck[1] != "yahoo.com" and emailCheck[1] != 'hotmail.com'and emailCheck[1] != 'pucit.edu.pk':
                return Response(response=render_template('register.html', msg="INVALID Email."))
            if len(passwd) < 8:
                return Response(response=render_template('register.html', msg="Password Length is too short."))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbAdmin = DbModelOfAdmin(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            objOfAdmin = admin(name, email, passwd, orgname, role, field)
            flag = dbAdmin.insertAdmin(objOfAdmin)
            if flag==True:
                session['adminName'] = name
                return Response(response=render_template('dashboard.html'), status=200, mimetype="text/html")
            return Response(response=render_template('register.html',msg='This admin name is not available. Please change the username'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class AdminLogin(Resource):
    def post(self):
        try:
            name = request.form.get("username")
            passwd = request.form.get("passwd")
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbAdmin = DbModelOfAdmin(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            flag = dbAdmin.login(name,passwd)
            if flag==True:
                session['adminName'] = name
                return Response(response=render_template('dashboard.html'), status=200, mimetype="text/html")
            return Response(response=render_template('login.html', msg="passwd and username is not match"))
        except Exception as e:
            print(str(e))
class CreateElection(Resource):
    def post(self):
        try:
            electionId = request.form.get("electionId")
            postion = request.form.get("postion")
            start_date = request.form.get("startDate")
            end_date = request.form.get("endDate")
            date_format = "%Y-%m-%d"
            startDate = datetime.strptime(start_date, date_format)
            endDate = datetime.strptime(end_date, date_format)
            if(startDate>=endDate):
                return Response(response=render_template('createElection.html', msg='end  date should be greater than start date'))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            adminName = session.get('adminName')
            electionObj = election(electionId, adminName, postion,startDate,endDate)
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            status=dbElection.getCheckElectionId(electionId)
            if (status == True):
                return Response(response=render_template('createElection.html', msg='This electionId is already used'))
            dbElection.insert(electionObj)
            session['electionId'] = electionId
            return Response(response=render_template('public.html'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class FileUpload(Resource):
    def post(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'],dbConfig['database'])
            file = request.files.get("file")
            file.save(f'uploads/{file.filename}')
            f = open(f'uploads/{file.filename}', "r")
            filename=file.filename
            filename=filename.split('.')
            if len(filename) == 1:
                return Response(response=render_template('public.html', msg="Please Upload Valid Syntax of File"))
            print(filename[1])
            if filename[1] != "txt":
                return Response(response=render_template('public.html', msg="INVALID File."))
            data = f.readlines()
            recordList = []
            electionId=session.get('electionId')
            for record in data:
                v = record.split(',')
                email=v[1]
                electionId=session.get('electionId')
                emailCheck = email.split('@')
                if len(emailCheck) == 1:
                    return Response(response=render_template('public.html', msg="Please upload Valid syntax of File"))
                dict = {'name': v[0], 'email': v[1]}
                recordList.append(dict)
            for record in recordList:
                v1 = voter(record['name'], record['email'],electionId)
                dbVoter.insert(v1)
            for record in recordList:
                voterId=dbVoter.getVoterId(record['email'],electionId)
                voterId=str(voterId)
                if (voterId != False):
                    name = record['name']
                    email_sender = 'evoting012@gmail.com'
                    email_password = 'dvtxwyycidsodenz'
                    email_reciever = record['email']
                    subject = 'you are added in new election'
                    body = """your username is """ + name + """ your id is """ + voterId + """ Keep it Secret Please"""
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_reciever
                    em['Subject'] = subject
                    em.set_content(body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_reciever, em.as_string())
            if(electionId==None):
                return Response(response=render_template('createElection.html',msg='please again enter election ID'))
            data = dbVoter.getAllData(electionId)
            return Response(response=render_template('selectCandidates.html',data=data), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class InsertCandidateData(Resource):
    def post(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            candidatesNumber = 0
            electionId=session.get('electionId')
            for getid in request.form.getlist('checkbox'):
                data = dbVoter.getVoterbyId(getid)
                for voterInfo in data:
                    candidateobj = candidate(voterInfo["username"], voterInfo["email"], voterInfo["electionId"])
                    flag=dbCandidate.insert(candidateobj)
                    candidatesNumber=candidatesNumber+1
            if(candidatesNumber<2):
                data = dbVoter.getAllData(electionId)
                return Response(response=render_template('selectCandidates.html',data=data, msg='Select at least 2 candidate'))
            if flag==True:
                return Response(response=render_template('dashboard.html',msg='candidates added succesfully'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class ElectionDetail(Resource):
    def post(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            electionId = request.form.get("electionId")
            adminName = session.get('adminName')
            valid = dbElection.checkValidElectionId(electionId, adminName)
            print(valid)
            if valid != True:
                return Response(response=render_template('electionDetail.html', msg="Wrong Election Id"), status=200,
                                mimetype="text/html")
            session['electionId']=electionId
            status=dbElection.getCheckElectionId(electionId)
            if(status==False):
                return Response(response=render_template('electionDetail.html',msg="Wrong Election Id"), status=200,
                                mimetype="text/html")
            return Response(response=render_template('electionDetailHomePage.html'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class GetAllVoters(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            electionId=session.get('electionId')
            data=dbVoter.getVotersbyElectionid(electionId)
            return Response(json.dumps(data), mimetype="application/json", status=200)
        except Exception as e:
            return ({"Error": str(e)}), 201
class GetAllCandidates(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            electionId = session.get('electionId')
            data=dbCandidate.getCandidatebyid(electionId)
            return Response(json.dumps(data), mimetype="application/json", status=200)
        except Exception as e:
            return ({"Error": str(e)}), 201

class ViewAllElection(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            adminName=session.get('adminName')
            data=dbElection.getAllRecords(adminName)
            return Response(json.dumps(data), mimetype="application/json", status=200)
        except Exception as e:
            return ({"Error": str(e)}), 201
class VoterLogin(Resource):
    def post(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'],dbConfig['database'])
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            name = request.form.get("username")
            id = request.form.get("id")
            electionId = dbVoter.getElectionId(id)
            flag1 = dbVoter.login(name, id)
            flag2=dbCandidate.CheckCandidateisVoter(electionId,name)
            if flag2==True:
                session['voterIsCandidate']='True'
            if flag1==True:
                session["electionId"] = electionId
                session["voterName"] = name
                session['voterId'] = id
                return Response(response=render_template('voterDashboard.html'),status=200,mimetype="text/html")
            else:
                return Response(response=render_template('login.html', msg='passwd and id is not match'),status=200,mimetype="text/html")
        except Exception as e:
            print(str(e))
class CastVote(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'],dbConfig['database'])
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                             dbConfig['database'])
            voterId=session.get('voterId')
            electionId=session.get('electionId')
            voterIsCandidate=session.get('voterIsCandidate')
            winnerName=dbCandidate.getWinner(electionId)
            dbElection.insertWinner(winnerName['username'],electionId)
            if (voterId == None or electionId == None):
                return Response(response=render_template('login.html', msg='first Login'))
            if voterIsCandidate=='True':
                return Response(response=render_template('voterDashboard.html', msg='you do not cast vote because you are candidate in this election'),
                                status=200, mimetype="text/html")
            endDate = dbElection.getEndDate(electionId)
            currentDate = date.today()
            if (currentDate >= endDate):
                return Response(response=render_template('voterDashboard.html', msg='time is out'),
                                status=200,
                                mimetype="text/html")
            data = dbCandidate.getCandidatebyid(electionId)
            voteStatus = dbVoter.getVote(voterId)
            if voteStatus == False:
                return Response(response=render_template('castVote.html',data=data),status=200,mimetype="text/html")
            return Response(response=render_template('voterDashboard.html',msg='you already cast Vote'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
    def post(self):
        try:
            voteStatus=False
            voterId=session.get('voterId')
            electionId=session.get('electionId')
            if (voterId == None or electionId == None):
                return Response(response=render_template('login.html', msg='first Login'))
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'], dbConfig['database'])
            for getid in request.form.getlist('radio'):
                voteStatus=True
                dbCandidate.updatevote(getid)
                dbVoter.SetVote(voterId)
            if(voteStatus==True):
                return Response(response=render_template('voterDashboard.html', msg="vote casted succesfully"),status=200,mimetype="text/html")
            else:
                data=dbCandidate.getCandidatebyid(electionId)
                return Response(response=render_template('castVote.html', data=data), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class ShowWinner(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                             dbConfig['database'])
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                             dbConfig['database'])
            voterId = session.get('voterId')
            electionId = session.get('electionId')
            if (voterId == None and electionId == None):
                return Response(response=render_template('login.html', msg='first Login'))
            endDate = dbElection.getEndDate(electionId)
            currentDate = date.today()
            if (currentDate < endDate):
                return Response(response=render_template('voterDashboard.html', msg='time is not out please wait'),
                                status=200,
                                mimetype="text/html")
            winner = dbCandidate.getWinner(electionId)
            if winner['noOfVote']!='0':
                return Response(response=render_template('getMaximumNoOfVote.html', data=winner),status=200,mimetype="text/html")
            return Response(response=render_template('voterDashboard.html',msg='No voter cast Vote'), status=200,
                            mimetype="text/html")
        except Exception as e:
            print(str(e))
class showElectionDetail(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                             dbConfig['database'])
            voterId = session.get('voterId')
            electionId = session.get('electionId')
            if (voterId == None and electionId == None):
                return Response(response=render_template('login.html', msg='first Login'))
            electionDetail = dbElection.getAllElectionDetailById(electionId)
            if electionDetail==False:
                return Response(response=render_template('login.html', msg='first login'),status=200,mimetype="text/html")
            return Response(response=render_template('electionDetaillnVoterDashboard.html',data=electionDetail), status=200,
                            mimetype="text/html")
        except Exception as e:
            print(str(e))
class ProfilepageOfAdmin(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbAdmin = DbModelOfAdmin(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                             dbConfig['database'])
            adminName=session.get('adminName')
            if adminName==None:
                return Response(response=render_template('register.html', msg='first Login'))
            data=dbAdmin.getDataForProfilePage(adminName)

            if data != False:
                return Response(response=render_template('profileAdmin.html', data=data),status=200,mimetype="text/html")
        except Exception as e:
            print(str(e))
class ProfilepageOfVoter(Resource):
    def get(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                             dbConfig['database'])
            voterId=session.get('voterId')
            if voterId==None:
                return Response(response=render_template('login.html', msg='first Login'))
            data=dbVoter.getDataForProfilePage(voterId)
            role=session.get('voterIsCandidate')
            if role=='True':
                role='Candidate'
            else:
                role='Voter'
            if data != False:
                return Response(response=render_template('profileVoter.html', data=data,role=role),status=200,mimetype="text/html")
        except Exception as e:
            print(str(e))
class ElectionRemoveById(Resource):
    def post(self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            electionId = request.form.get("electionId")
            status = dbElection.getCheckElectionId(electionId)
            if (status == False):
                return Response(response=render_template('electionDetail.html', msg="Wrong Election Id"), status=200,
                                mimetype="text/html")
            dbVoter.removeVoterByElectionId(electionId)
            dbCandidate.removeCandidateByElectionId(electionId)
            dbElection.removeByElectionId(electionId)
            return Response(response=render_template('dashboard.html',msg='succesfull remove election'), status=200, mimetype="text/html")
        except Exception as e:
            print(str(e))
class DeactivateAdminAccount(Resource):
    def delete (self):
        try:
            global duplicateApp
            dbConfig = dbDictionary(duplicateApp)
            dbElection = DbModelOfElection(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            dbVoter = DbModelOfVoter(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            dbCandidate = DbModelOfCandidate(dbConfig['host'], dbConfig['user'], dbConfig['password'],
                                           dbConfig['database'])
            dbAdmin = DbModelOfAdmin(dbConfig['host'], dbConfig['user'], dbConfig['password'],dbConfig['database'])
            adminName=session.get('adminName')
            electionIdlist=dbElection.getAllElectionId(adminName)
            if electionIdlist!=None:
                for electionId in electionIdlist:
                    dbVoter.removeVoterByElectionId(electionId['electionId'])
                    dbCandidate.removeCandidateByElectionId(electionId['electionId'])
                    dbElection.removeByElectionId(electionId['electionId'])
            dbAdmin.deactivateAccount(adminName)
            return '1'
        except Exception as e:
            print(str(e))