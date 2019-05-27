import unittest
from test_function import Functions

class Test(unittest.TestCase):

    def test_addHospital(self):
        hosp1 = Functions()
        name = hosp1.hospital_name = "CCMC"
        address = hosp1.hospital_address= "Mandaue City"
        email = hosp1.hospital_email ="ccmc@gmail.com"
        contact = hosp1.hospital_contact = 4178247
        password = hosp1.hospital_password = "ccmcadmin"
        h_type = hosp1.hospital_type = "public"  

        hospital = hosp1.addHospital(name,address,email,contact,password,h_type)
        self.assertIsNotNone(hospital)

    def test_addUser(self):
        user1 = Functions()
        fname = user1.user_firstname = "Joanna"
        mname = user1.user_middlename= "Mendoza"
        lname = user1.user_lastname ="Pasa"
        email = user1.user_email = "joan@gmail.com"
        password = user1.user_password = "joannapasa"
        fcm = user1.fcm_token = "SJKA1315ASD13"  

        user = user1.addUser(fname,mname,lname,email,password,fcm)
        self.assertIsNotNone(user)

    def test_addResponder(self):
        resp1 = Functions()
        fname = resp1.responder_firstname = "Timmy"
        mname = resp1.responder_middlename= "Donaire"
        lname = resp1.responder_lastname ="Guron"  

        resp = resp1.addResponder(fname,mname,lname)
        self.assertIsNotNone(resp)

    def test_addReport(self):
        report1 = Functions()
        img = report1.report_image = "accident.jpg"
        loc = report1.report_location= "Cebu City"
        r_type = report1.report_type ="accident"  
        others = report1.report_others ="head injury"  
        status = report1.report_status ="pending"  

        report = report1.addReport(img,loc,r_type,others,status)
        self.assertIsNotNone(report)

if __name__ == '__main__':
    unittest.main()