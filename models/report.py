from google.appengine.ext import ndb

class Report(ndb.Model):
    report_image = ndb.StringProperty()
    report_location = ndb.StringProperty()
    report_type = ndb.StringProperty()
    report_others = ndb.StringProperty()
    report_status = ndb.StringProperty()
    user = ndb.KeyProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def addReport(cls,user_id,report_image,report_location,report_type,report_others,report_status):
            
        report = cls()

        user_id = str(user_id)
        if user_id.isdigit():
            user_key = ndb.Key('User',int(user_id))
            report.user = user_key

        if report_image:
            report.report_image = report_image
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

    @classmethod
    def updateReport(cls,report_id,report_status):

        report = cls.get_by_id(int(report_id))

        if report_status:
            report.report_status = report_status

        report.put()
        return report

    
    @classmethod
    def getAccidentsCount(cls):

        accidentCount=0
        accidents = cls.query(cls.report_type=="Accident").fetch()

        for a in accidents:
            accidentCount = accidentCount + 1
        
        return accidentCount
    
    @classmethod
    def getPregnancyCount(cls):

        pregnancyCount=0
        pregnancy = cls.query(cls.report_type=="Pregnancy").fetch()

        for p in pregnancy:
            pregnancyCount = pregnancyCount + 1
        
        return pregnancyCount
    
    @classmethod
    def getIllnessCount(cls):

        illnessCount=0
        illness = cls.query(cls.report_type=="Illness").fetch()

        for i in illness:
            illnessCount = illnessCount +1
        
        return illnessCount
    @classmethod
    def getRecentReports(cls):

        count=0
        limit=3
        recentReports = []

        reports = Report.query().order(-cls.created).fetch()

        for r in reports:
            if count != limit:
                countAdded = r.to_dict()
                countAdded["count"] =count
                recentReports.append(countAdded)
                count =count + 1

        return recentReports
        

    def to_dict(self):
        data = {}
        data['id'] = self.key.id()
        data['report_location'] = self.report_location
        data['report_type'] = self.report_type
        data['report_others'] = self.report_others
        data['report_image'] = self.report_image
        data['report_status'] = self.report_status
        data['created'] = self.created.isoformat() + "Z"
        return data

    def report_dict(self):
        data = {}
        data['report_location'] = self.report_location
        data['report_type'] = self.report_type 
        data['report_image'] = self.report_image
        data['created'] = self.created.isoformat() + "Z"