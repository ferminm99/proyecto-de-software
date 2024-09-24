import unittest
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

def chek_attr_value_user(testU, user=None, email=None, username=None, password=None, 
                         first_name=None, last_name=None, active=None, approved=None):
    testU.assertEqual(user.email, email)
    testU.assertEqual(user.username, username)
    testU.assertEqual(user.password, password)
    testU.assertEqual(user.first_name, first_name)
    testU.assertEqual(user.last_name, last_name)
    testU.assertEqual(user.active, active)
    testU.assertEqual(user.approved, approved)

class TestUser(unittest.TestCase):
    
    def setUp(self):
        
        permission1= Permission()
        permission1.id = 0
        permission1.name = "user_index"
        
        permission2= Permission()
        permission2.id = 1
        permission2.name = "user_new"
        
        permission3= Permission()
        permission3.id = 2
        permission3.name = "user_update"
        
        permission4= Permission()
        permission4.id = 3
        permission4.name = "user_destroy"
        
        self.permissionsAdm=[permission1, permission2, permission3, permission4]
        self.permissionsOpe=[permission1]
        
        roleAdm = Role()
        roleAdm.id=0
        roleAdm.name="Administrador"
        roleAdm.permissions.append(permission1)
        roleAdm.permissions.append(permission2)
        roleAdm.permissions.append(permission3)
        roleAdm.permissions.append(permission4)
        
        roleOpe = Role()
        roleOpe.id=1
        roleOpe.name="Operador"
        roleOpe.permissions.append(permission1)
        
        self.user1= User(
            email="user1@gmail.com", username="username1", password="pass1", 
            first_name="first_name1", last_name="last_name1", active="1", approved="1")
        self.user1.roles.append(roleOpe)
        self.user1.roles.append(roleAdm)
        
        self.user2= User(
            email="user2@gmail.com", username="username2", password="pass2", 
            first_name="first_name2", last_name="last_name2", active="1", approved="1")
        self.user2.roles.append(roleOpe)
        
        self.user3= User(
            email="user3@gmail.com", username="username3", password="pass3", 
            first_name="first_name3", last_name="last_name3", active="0", approved="0")
        
        longPhrase = "11"
        for x in range(10):
            longPhrase = longPhrase+longPhrase
        self.longPhrase = longPhrase
        
        self.user4= User(
            email=longPhrase, username=longPhrase, password=longPhrase, 
            first_name=longPhrase, last_name=longPhrase, active=longPhrase, approved=longPhrase)
        
        self.user5= User(
            email="", username="", password="", 
            first_name="", last_name="", active="", approved="")
        
        self.user6= User(
            email=None, username=None, password=None, 
            first_name=None, last_name=None, active=None, approved=None)
    
    def test_init(self):
        
        user1= User(
            email="user1@gmail.com", username="username1", password="pass1", 
            first_name="first_name1", last_name="last_name1", active="0", approved="0")
        self.assertIsInstance(user1, User)
        chek_attr_value_user(
            self, user1, email="user1@gmail.com", username="username1", password="pass1", 
            first_name="first_name1", last_name="last_name1", active="0", approved="0")
        
        user2= User(
            email="user2@gmail.com", username="username2", password="pass2", 
            first_name="first_name2", last_name="last_name2", active="1", approved="0")
        self.assertIsInstance(user2, User)
        chek_attr_value_user(
            self, user2, email="user2@gmail.com", username="username2", password="pass2", 
            first_name="first_name2", last_name="last_name2", active="1", approved="0")
        
        user3= User(
            email="user3@gmail.com", username="username3", password="pass3", 
            first_name="first_name3", last_name="last_name3", active="0", approved="1")
        self.assertIsInstance(user3, User)
        chek_attr_value_user(
            self, user3, email="user3@gmail.com", username="username3", password="pass3", 
            first_name="first_name3", last_name="last_name3", active="0", approved="1")
        
        user4= User(
            email="user4@gmail.com", username="username4", password="pass4", 
            first_name="first_name4", last_name="last_name4", active="1", approved="1")
        self.assertIsInstance(user4, User)
        chek_attr_value_user(
            self, user4, email="user4@gmail.com", username="username4", password="pass4", 
            first_name="first_name4", last_name="last_name4", active="1", approved="1")
        
        longPhrase = self.longPhrase
    
        user5= User(
            email=longPhrase, username=longPhrase, password=longPhrase, 
            first_name=longPhrase, last_name=longPhrase, active=longPhrase, approved=longPhrase)
        self.assertIsInstance(user5, User)
        chek_attr_value_user(
            self, user5, email=longPhrase, username=longPhrase, password=longPhrase, 
            first_name=longPhrase, last_name=longPhrase, active=longPhrase, approved=longPhrase)
        
        user6= User(
            email="", username="", password="", 
            first_name="", last_name="", active="", approved="")
        self.assertIsInstance(user6, User)
        chek_attr_value_user(
            self, user6, email="", username="", password="", 
            first_name="", last_name="", active="", approved="")
        
        user7= User(
            email=None, username=None, password=None, 
            first_name=None, last_name=None, active=None, approved=None)
        self.assertIsInstance(user7, User)
        chek_attr_value_user(
            self, user7, email=None, username=None, password=None, 
            first_name=None, last_name=None, active=None, approved=None)
    
    def test_havePermission(self):
        
        #Check User Admin Permissions
        self.assertFalse(self.user1.havePermission(["permiso inexistente"]))
        self.assertFalse(self.user1.havePermission(
            ["user_index","user_new","user_update","user_destroy", "permiso inexistente"]))
        self.assertTrue(self.user1.havePermission(
            ["user_index","user_new","user_update","user_destroy"]))
        self.assertTrue(self.user1.havePermission([]))
        
        #Check User Operator Permissions
        self.assertFalse(self.user2.havePermission(["permiso inexistente"]))
        self.assertFalse(self.user2.havePermission(
            ["user_index","user_new","user_update","user_destroy"]))
        self.assertFalse(self.user2.havePermission(["user_destroy"]))
        self.assertTrue(self.user2.havePermission(["user_index"]))
        self.assertTrue(self.user2.havePermission([]))
        
        #Check User without Role Permissions
        self.assertFalse(self.user3.havePermission(["permiso inexistente"]))
        self.assertFalse(self.user3.havePermission(["user_index"]))
        self.assertTrue(self.user3.havePermission([]))
        
        
    def test_isAdmin(self):
        self.assertTrue(self.user1.isAdmin())
        self.assertFalse(self.user2.isAdmin())

if __name__ == "__main__":
    unittest.main()