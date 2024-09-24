import unittest
from app.models.meetingpoint import MeetingPoint

def chek_attr_value_meetingpoint(testMP,meetingpoint=None, name=None, address=None, state=None, 
                                 telephone=None, email=None, latitude=None, length=None):
    testMP.assertEqual(meetingpoint.name, name)
    testMP.assertEqual(meetingpoint.address, address)
    testMP.assertEqual(meetingpoint.state, state)
    testMP.assertEqual(meetingpoint.telephone, telephone)
    testMP.assertEqual(meetingpoint.email, email)
    testMP.assertEqual(meetingpoint.latitude, latitude)
    testMP.assertEqual(meetingpoint.length, length)

def format_as_dict_meetingpoint(meetingpoint):
       return {"id": meetingpoint.id , "name":meetingpoint.name, 
              "address":meetingpoint.address, "state":meetingpoint.state, 
              "telephone":meetingpoint.telephone, "email":meetingpoint.email, 
              "latitude":meetingpoint.latitude, "length":meetingpoint.length}

class TestMeetingPoint(unittest.TestCase):
    
    def setUp(self):
        self.meetingpoint1= MeetingPoint(
               name="Punto1", address="26 entre 2 y 3", state=0, 
               telephone="5267288", email="punto1@gmail.com", 
               latitude="1800", length="1500")
        self.meetingpoint2= MeetingPoint(
               name="Punto2", address="3 entre 1 y 5", state=-9999, 
               telephone="9463321", email="punto2@hotmail.com", 
               latitude="233", length="5033")
        longPhrase = "11"
        for x in range(10):
            longPhrase = longPhrase+longPhrase
        self.longPhrase = longPhrase
        self.meetingpoint3= MeetingPoint(
               name=longPhrase, address=longPhrase, state=9999, 
               telephone=longPhrase, email=longPhrase, 
               latitude=longPhrase, length=longPhrase)
        self.meetingpoint4= MeetingPoint(
               name="", address="", state=0, telephone="", 
               email="", latitude="", length="")
        self.meetingpoint5= MeetingPoint(
               name=None, address=None, state=None, telephone=None, 
               email=None, latitude=None, length=None)
    
    def test_init(self):
        meetingpoint1 = MeetingPoint(
               name="Punto1", address="26 entre 2 y 3", state=0, 
               telephone="5267288", email="punto1@gmail.com", 
               latitude="1800", length="1500")
        self.assertIsInstance(meetingpoint1, MeetingPoint)
        chek_attr_value_meetingpoint(
               self, meetingpoint1, "Punto1", "26 entre 2 y 3", 0,
               "5267288", "punto1@gmail.com", "1800", "1500")
        meetingpoint2 = MeetingPoint(
               name="Punto2", address="3 entre 1 y 5", state=-9999, 
               telephone="9463321", email="punto2@hotmail.com", 
               latitude="233", length="5033")
        self.assertIsInstance(meetingpoint2, MeetingPoint)
        chek_attr_value_meetingpoint(
               self, meetingpoint2, "Punto2", "3 entre 1 y 5", -9999,
               "9463321", "punto2@hotmail.com", "233", "5033")
        longPhrase = self.longPhrase
        meetingpoint3 = MeetingPoint(
               name=longPhrase, address=longPhrase, state=9999, 
               telephone=longPhrase, email=longPhrase, 
               latitude=longPhrase, length=longPhrase)
        self.assertIsInstance(meetingpoint3, MeetingPoint)
        chek_attr_value_meetingpoint(
               self, meetingpoint3, longPhrase, longPhrase, 9999,
               longPhrase, longPhrase, longPhrase, longPhrase)
        meetingpoint4 = MeetingPoint(
               name="", address="", state=0, telephone="", 
               email="", latitude="", length="")
        self.assertIsInstance(meetingpoint4, MeetingPoint)
        chek_attr_value_meetingpoint(
               self, meetingpoint4, "", "", 0, "", "", "", "")
        meetingpoint5 = MeetingPoint(
               name=None, address=None, state=None, telephone=None, 
               email=None, latitude=None, length=None)
        self.assertIsInstance(meetingpoint5, MeetingPoint)
        chek_attr_value_meetingpoint(
               self, meetingpoint5, None, None, None, None, None, None, None)
    
    def test_as_dict(self):
        self.assertDictEqual(
               format_as_dict_meetingpoint(self.meetingpoint1), 
               self.meetingpoint1.as_dict())
        self.assertDictEqual(
               format_as_dict_meetingpoint(self.meetingpoint2), 
               self.meetingpoint2.as_dict())
        self.assertDictEqual(
               format_as_dict_meetingpoint(self.meetingpoint3), 
               self.meetingpoint3.as_dict())
        self.assertDictEqual(
               format_as_dict_meetingpoint(self.meetingpoint4), 
               self.meetingpoint4.as_dict())
        self.assertDictEqual(
               format_as_dict_meetingpoint(self.meetingpoint5), 
               self.meetingpoint5.as_dict())

if __name__ == "__main__":
    unittest.main()