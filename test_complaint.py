import unittest
from datetime import datetime
from app.models.complaint import Complaint

def chek_attr_value_complaint(testC, complaint, title=None, id_category=None, closed_at=None, email=None, latitude=None, 
                                 length=None, id_state=None, id_user_assigned=None, first_name=None, last_name=None, 
                                 telephone=None, description=None, address=None):
    testC.assertEqual(complaint.title, title)
    testC.assertEqual(complaint.id_category, id_category)
    testC.assertEqual(complaint.closed_at, closed_at)
    testC.assertEqual(complaint.email, email)
    testC.assertEqual(complaint.latitude, latitude)
    testC.assertEqual(complaint.length, length)
    testC.assertEqual(complaint.id_state, id_state)
    testC.assertEqual(complaint.id_user_assigned, id_user_assigned)
    testC.assertEqual(complaint.first_name, first_name)
    testC.assertEqual(complaint.last_name, last_name)
    testC.assertEqual(complaint.telephone, telephone)
    testC.assertEqual(complaint.description, description)
    testC.assertEqual(complaint.address, address)

def format_as_dict_complaint(complaint):
    return {"id":complaint.id, "title":complaint.title, 
            "id_category":complaint.id_category, "description":complaint.description, 
            "address":complaint.address, "created_at":complaint.created_at,
            "closed_at":complaint.closed_at, "latitude":complaint.latitude,
            "length":complaint.length, "id_state":complaint.id_state,
            "id_user_assigned":complaint.id_user_assigned, 
            "first_name":complaint.first_name, "last_name":complaint.last_name,
            "telephone":complaint.telephone, "email":complaint.email}

class TestComplaint(unittest.TestCase):
    
    def setUp(self):
        self.complaint1= Complaint(
            title="title1", id_category=1, closed_at=datetime.now(), email="comp1@gmail.com", 
            latitude=1200, length=1100, id_state=1, id_user_assigned=1, first_name="first_name", 
            last_name="last_name", telephone="46385435", description="description...", address="direction1")
        longPhrase = "11"
        for x in range(10):
            longPhrase = longPhrase+longPhrase
        self.longPhrase = longPhrase
        self.complaint2= Complaint(
            title=longPhrase, id_category=999999, closed_at=datetime.now(), email=longPhrase, 
            latitude=999999, length=999999, id_state=999999, id_user_assigned=999999, first_name=longPhrase, 
            last_name=longPhrase, telephone=longPhrase, description=longPhrase, address=longPhrase)
        self.complaint3= Complaint(
            title="title1", id_category=-1, closed_at=datetime.now(), email="comp1@gmail.com", 
            latitude=-1200, length=-1100, id_state=1, id_user_assigned=-1, first_name="first_name", 
            last_name="last_name", telephone="46385435", description="description...", address="direction1")
        self.complaint4= Complaint(
            title="", id_category=0, closed_at=datetime.now(), email="", 
            latitude=0, length=0, id_state=0, id_user_assigned=0, first_name="", 
            last_name="", telephone="", description="", address="")
        self.complaint5= Complaint(
            title=None, id_category=None, closed_at=None, email=None, 
            latitude=None, length=None, id_state=None, id_user_assigned=None, first_name=None, 
            last_name=None, telephone=None, description=None, address=None)
    
    def test_init(self):
        complaint1= Complaint(
            title="title1", id_category=1, closed_at=datetime.now(), email="comp1@gmail.com", 
            latitude=1200, length=1100, id_state=1, id_user_assigned=1, first_name="first_name", 
            last_name="last_name", telephone="46385435", description="description...", address="direction1")
        self.assertIsInstance(complaint1, Complaint)
        chek_attr_value_complaint(
            self, complaint1, title="title1", id_category=1, closed_at=datetime.now(), 
            email="comp1@gmail.com", latitude=1200, length=1100, id_state=1, 
            id_user_assigned=1, first_name="first_name", last_name="last_name", 
            telephone="46385435", description="description...", address="direction1")
        longPhrase = self.longPhrase
        complaint2= Complaint(
            title=longPhrase, id_category=999999, closed_at=datetime.now(), email=longPhrase, 
            latitude=999999, length=999999, id_state=999999, id_user_assigned=999999, first_name=longPhrase, 
            last_name=longPhrase, telephone=longPhrase, description=longPhrase, address=longPhrase)
        self.assertIsInstance(complaint2, Complaint)
        chek_attr_value_complaint(
            self, complaint2, title=longPhrase, id_category=999999, closed_at=datetime.now(), 
            email=longPhrase, latitude=999999, length=999999, id_state=999999, 
            id_user_assigned=999999, first_name=longPhrase, last_name=longPhrase, 
            telephone=longPhrase, description=longPhrase, address=longPhrase)
        complaint3= Complaint(
            title="title1", id_category=-1, closed_at=datetime.now(), email="comp1@gmail.com", 
            latitude=-1200, length=-1100, id_state=1, id_user_assigned=-1, first_name="first_name", 
            last_name="last_name", telephone="46385435", description="description...", address="direction1")
        self.assertIsInstance(complaint3, Complaint)
        chek_attr_value_complaint(
            self, complaint3, title="title1", id_category=-1, closed_at=datetime.now(), email="comp1@gmail.com", 
            latitude=-1200, length=-1100, id_state=1, id_user_assigned=-1, first_name="first_name", 
            last_name="last_name", telephone="46385435", description="description...", address="direction1")
        complaint4= Complaint(
            title="", id_category=0, closed_at=datetime.now(), email="", 
            latitude=0, length=0, id_state=0, id_user_assigned=0, first_name="", 
            last_name="", telephone="", description="", address="")
        self.assertIsInstance(complaint4, Complaint)
        chek_attr_value_complaint(
            self, complaint4, title="", id_category=0, closed_at=datetime.now(), email="", 
            latitude=0, length=0, id_state=0, id_user_assigned=0, first_name="", 
            last_name="", telephone="", description="", address="")
        complaint5= Complaint(
            title=None, id_category=None, closed_at=None, email=None, 
            latitude=None, length=None, id_state=None, id_user_assigned=None, first_name=None, 
            last_name=None, telephone=None, description=None, address=None)
        self.assertIsInstance(complaint5, Complaint)
        chek_attr_value_complaint(
            self, complaint5, title=None, id_category=None, closed_at=None, email=None, 
            latitude=None, length=None, id_state=None, id_user_assigned=None, first_name=None, 
            last_name=None, telephone=None, description=None, address=None)
    
    def test_as_dict(self):
        self.assertDictEqual(
            format_as_dict_complaint(self.complaint1),
            self.complaint1.as_dict())
        self.assertDictEqual(
            format_as_dict_complaint(self.complaint2),
            self.complaint2.as_dict())
        self.assertDictEqual(
            format_as_dict_complaint(self.complaint3),
            self.complaint3.as_dict())
        self.assertDictEqual(
            format_as_dict_complaint(self.complaint4),
            self.complaint4.as_dict())
        self.assertDictEqual(
            format_as_dict_complaint(self.complaint5),
            self.complaint5.as_dict())
    
    def test_getId(self):
        self.assertEqual(self.complaint1.id, self.complaint1.getId())
        self.assertEqual(self.complaint2.id, self.complaint2.getId())
        self.assertEqual(self.complaint3.id, self.complaint3.getId())
        self.assertEqual(self.complaint4.id, self.complaint4.getId())
        self.assertEqual(self.complaint5.id, self.complaint5.getId())

if __name__ == "__main__":
    unittest.main()