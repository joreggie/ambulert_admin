from google.appengine.ext import ndb
from models.hospital import Hospital

class User(ndb.Model):
    hospital = ndb.KeyProperty(kind=Hospital)
    user_firstname = ndb.StringProperty()
    user_middlename= ndb.StringProperty()
    user_lastname= ndb.StringProperty()
    user_email= ndb.StringProperty()
    fcm_token = ndb.StringProperty()
    user_password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addUser(cls,user_firstname,user_middlename,user_lastname,user_email,user_password,fcm_token):
        
        user = cls()

        if user_firstname:
            user.user_firstname = user_firstname
        if user_middlename:
            user.user_middlename = user_middlename
        if user_lastname:
            user.user_lastname = user_lastname
        if user_email:
            user.user_email = user_email
        if user_password:
            user.user_password = user_password
        if fcm_token:
            user.fcm_token = fcm_token   

        user.put()
        return user
    @classmethod
    def updateHospitalUser(cls,user_id,hospital_id):

        user = cls.get_by_id(int(user_id))

        hospital_id = str(hospital_id)
        if hospital_id.isdigit():
            hospital_key = ndb.Key('Hospital',int(hospital_id))
            user.hospital = hospital_key

        user.put()
        return user

    @classmethod 
    def addToken(cls,user_id,token):

        user = cls.get_by_id(int(user_id))

        if token:
            user.fcm_token = token

        user.put()
        return user 
    
    @classmethod 
    def signinUser(cls,user_email,user_password):
        user = None

        if user_email and user_password:
            user = cls.query(cls.user_email == user_email, cls.user_password == user_password).get()
        
        if user == None:
            user == None

        return user

    def to_dict(self):
        data = {}
        
        data['user_firstname'] = self.user_firstname
        data['user_middlename'] = self.user_middlename
        data['user_lastname'] = self.user_lastname
        data['user_email'] = self.user_email
        data['created'] = self.created.isoformat() + 'Z'
        return data  