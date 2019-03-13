from google.appengine.ext import ndb

class User(ndb.Model):
    user_firstname = ndb.StringProperty()
    user_middlename= ndb.StringProperty()
    user_lastname= ndb.StringProperty()
    user_email= ndb.StringProperty()
    user_password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addUser(cls,user_firstname,user_middlename,user_lastname,user_email,user_password):
        
        user = cls()

        if user_firstname:
            user.user_name = user_firstname
        if user_middlename:
            user.user_middlename = user_middlename
        if user_lastname:
            user.user_lastname = user_lastname
        if user_email:
            user.user_email = user_email
        if user_password:
            user.user_password = user_password   

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