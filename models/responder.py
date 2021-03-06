from google.appengine.ext import ndb
from models.hospital import Hospital

class Responder(ndb.Model):
    hospital = ndb.KeyProperty(kind=Hospital)
    responder_firstname = ndb.StringProperty()
    responder_middlename = ndb.StringProperty()
    responder_lastname = ndb.StringProperty()
    report_info = ndb.KeyProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addResponder(cls,hospital_id,responder_firstname,responder_middlename,responder_lastname,report_info):
            
        responder = cls()

        hospital_id = str(hospital_id)
        if hospital_id.isdigit():
            hospital_key = ndb.Key('Hospital',int(hospital_id))
            responder.hospital = hospital_key
        
        if responder_firstname:
            responder.responder_firstname = responder_firstname
        if responder_middlename:
            responder.responder_middlename = responder_middlename
        if responder_lastname:
            responder.responder_lastname = responder_lastname
        if report_info:
            responder.report_info = report_info

        responder.put()
        return responder

    @classmethod
    def assignRescue(cls,responder_id,report_info):

        responder = cls.get_by_id(int(responder_id))

        report_id = str(report_info)
        if report_id.isdigit():
            report_key = ndb.Key('Report',int(report_id))
            responder.report_info = report_key

        responder.put()
        return responder

    @classmethod
    def getReportInfo(cls, responder_id):

        report_info = None

        if responder_id:
            responder = cls.get_by_id(int(responder_id))
            if responder:
                report_info = responder.to_dict()
        
        return report_info

    @classmethod
    def updateResponder(cls,responder_id,responder_firstname,responder_middlename,responder_lastname):

        responder = cls.get_by_id(int(responder_id))
        if responder_firstname:
            responder.responder_firstname = responder_firstname
        if responder_middlename:
            responder.responder_middlename = responder_middlename
        if responder_lastname:
            responder.responder_lastname = responder_lastname

        responder.put()
        return responder

    def dispatch(self):
        data = {}
        data['id'] = self.key.id()
        data['responder_firstname'] = self.responder_firstname
        data['responder_lastname'] = self.responder_lastname
        data['report_info'] = self.report_info
        data['created'] = self.created.isoformat() + 'Z'
        return data

    def to_dict(self):
        data = {}
        data['id'] = self.key.id()
        data['hospital'] = None
        if self.hospital:
            hospital = self.hospital.get()
            data['hospital'] = hospital.to_dict()

        data['report_info'] = None
        if self.report_info:
            report = self.report_info.get()
            data['report_info'] = report.to_dict()

        data['responder_firstname'] = self.responder_firstname
        data['responder_middlename'] = self.responder_middlename
        data['responder_lastname'] = self.responder_lastname
        data['created'] = self.created.isoformat() + 'Z'
        return data