from .resources import *
def initialize_routes(api):
    api.add_resource(AdminSignup,'/api/adminsignup')
    api.add_resource(AdminLogin, '/api/adminlogin')
    api.add_resource(CreateElection, '/api/createElection')
    api.add_resource(FileUpload, '/api/FileUpload')
    api.add_resource(InsertCandidateData,'/api/InsertCandidateData')
    api.add_resource(ViewAllElection, '/api/ViewAllElection')
    api.add_resource(ElectionDetail, '/api/ElectionDetail')
    api.add_resource(GetAllVoters, '/api/GetAllVoters')
    api.add_resource(GetAllCandidates, '/api/GetAllCandidates')
    api.add_resource(VoterLogin, '/api/VoterLogin')
    api.add_resource(CastVote, '/api/CastVote')
    api.add_resource(ShowWinner, '/api/ShowWinner')
    api.add_resource(showElectionDetail, '/api/showElectionDetail')
    api.add_resource(ProfilepageOfAdmin, '/api/ProfilepageOfAdmin')
    api.add_resource(ProfilepageOfVoter, '/api/ProfilepageOfVoter')
    api.add_resource(ElectionRemoveById, '/api/ElectionRemoveById')
    api.add_resource(DeactivateAdminAccount, '/api/DeactivateAdminAccount')












