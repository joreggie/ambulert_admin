from google.appengine.ext import ndb

class Report(ndb.Model):
    report_location = ndb.StringProperty()
    report_type = ndb.StringProperty()
    report_others = ndb.StringProperty()
    report_status = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addReport(cls,report_location,report_type,report_others,report_status):
            
        report = cls()

        if report_location:
            report.report_location = report_location
        if report_type:
            report.report_type = report_type
        if report_others:
            report.report_others = report_others
        if report_status:
            report.report_status = report_status
    
        report.put()
        return report
    
    

    def to_dict(self):
        data = {}
        data['id'] = self.key.id()
        data['report_location'] = self.report_location
        data['report_type'] = self.report_type
        data['report_others'] = self.report_others
        data['report_status'] = self.report_status
        data['created'] = self.created.isoformat() + "Z"
        return data