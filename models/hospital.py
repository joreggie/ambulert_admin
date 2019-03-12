from google.appengine.ext import ndb

class Hospital(ndb.Model):
    hospital_name = ndb.StringProperty()
    hospital_address = ndb.StringProperty()
    hospital_email = ndb.StringProperty()
    hospital_contact = ndb.StringProperty()
    hospital_password = ndb.StringProperty()
    hospital_type = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addHospital(cls,hospital_name,hospital_address,hospital_email,hospital_contact,hospital_password,hospital_type):
        
        hospital = cls()

        if hospital_name:
            hospital.hospital_name = hospital_name
        if hospital_address:
            hospital.hospital_address = hospital_address
        if hospital_email:
            hospital.hospital_email = hospital_email
        if hospital_contact:
            hospital.hospital_contact = hospital_contact
        if hospital_password:
            hospital.hospital_password = hospital_password   
        if hospital_type:
            hospital.hospital_type = hospital_type

        hospital.put()
        return hospital
    
    @classmethod 
    def signinHospital(cls,hospital_email,hospital_password):
        admin = None

        if hospital_email and hospital_password:
            admin = cls.query(cls.hospital_email == hospital_email, cls.hospital_password == hospital_password).get()
        
        if admin == None:
            admin == None

        return admin