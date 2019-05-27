class Functions():
    
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
            hospital.hospital_password =hospital_password
        if hospital_type:
            hospital.hospital_type = hospital_type

        return hospital
    
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

        return user
    
    @classmethod
    def addResponder(cls,responder_firstname,responder_middlename,responder_lastname):
            
        responder = cls()
        
        if responder_firstname:
            responder.responder_firstname = responder_firstname
        if responder_middlename:
            responder.responder_middlename = responder_middlename
        if responder_lastname:
            responder.responder_lastname = responder_lastname

        return responder

    @classmethod
    def addReport(cls,report_image,report_location,report_type,report_others,report_status):
            
        report = cls()

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
    
        return report
