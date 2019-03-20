from google.appengine.ext import ndb

class Report(ndb.Model):
    report_location = ndb.StringProperty()
    report_type = ndb.StringProperty()
    report_others = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addReport(cls,report_location,report_type,report_others):
            
        report = cls()

        if report_location:
            report.report_location = report_location
        if report_type:
            report.report_type = report_type
        if report_others:
            report.report_others = report_others
    
        report.put()
        return report   