#hey
from flask import Flask,request,render_template,Response,session
from flask_restful import Api,Resource
from flask_session import Session
from resources import routes,resources
from database.DbHandlerClasses import *
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.secret_key=app.config['SECRET_KEY']
api = Api(app) #instansiate api's
routes.initialize_routes(api) #initialize routes
resources.copyAppInstance(app) #coppying app instance in resource.py for db configurations

@app.route('/')
def welcome():
    return 'welcome to voting system'

@app.route('/home')
def homepage():
    return render_template("home.html")

@app.route('/aboutUs')
def aboutUsPage():
    return render_template("aboutUs.html")

@app.route('/help')
def helpPage():
    return render_template("help.html")

@app.route('/signupAdmin')
def registerPage():
    return render_template("register.html")

@app.route('/loginOfAdmin')
def login_admin():
    return render_template("login.html")

@app.route('/dashboard')
def dashboardPage():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account ')
    return render_template("dashboard.html")

@app.route('/createElection')
def create_Election():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account ')
    return render_template('createElection.html')

@app.route('/viewAllElection')
def viewAll_Election():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account ')
    return render_template('viewAllElection.html')

@app.route('/removeElection')
def removeElection():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account ')
    return render_template('removeSpecificElection.html')

@app.route('/electionDetail')
def electionDetail():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account')
    return render_template('electionDetail.html')

@app.route('/electionDetailHomePage')
def electionDetailHome():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account')
    return render_template('electionDetailHomePage.html')

@app.route('/voterDisplay')
def votersDisplay():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account')
    return render_template('voterDisplay.html')

@app.route('/candidateDisplay')
def candidatesDisplay():
    adminName = session.get('adminName')
    if (adminName == None):
        return render_template('register.html', msg='first create account')
    return render_template('candidateDisplay.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/voterlogin')
def login_voter():
    return render_template('login.html')

@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/voterDashboard')
def voterDashboard():
    return render_template('voterDashboard.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

if __name__ == '__main__':
    app.run()
