from google.appengine.ext import ndb

class Responder(ndb.Model):
    responder_firstname = ndb.StringProperty()
    responder_middlename = ndb.StringProperty()
    responder_lastname = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addResponder(cls,responder_firstname,responder_middlename,responder_lastname):
            
        responder = cls()

        if responder_firstname:
            responder.responder_firstname = responder_firstname
        if responder_middlename:
            responder.responder_middlename = responder_middlename
        if responder_lastname:
            responder.responder_lastname = responder_lastname
    
        responder.put()
        return responder   