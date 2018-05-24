import unittest
import json
from app import create_app, db

class QuestionTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.question = {'question': 'what is 5000*2345?','answer':'11725000','distractor':'11540003,45892053'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
            user_data = {
                'email': email,
                'password': password
            }
            return( self.client().post('/auth/register', data=user_data))

    def login_user(self, email="user@test.com", password="test1234"):
            user_data = {
                'email': email,
                'password': password
            }
            return( self.client().post('/auth/login', data=user_data))

    def test_question_creation(self):
        """Test the API can create a question"""
        self.register_user()
        user= self.login_user()
        Access_token=json.loads(user.data.decode())['access_token']
        res= self.client().post(
            '/questions/',
            headers=dict(Authorization="Bearer "+Access_token),
            data= self.question
        )

    def test_question_can_get_all(self):
        """Test the API can read all a questions"""
        self.register_user()
        user= self.login_user()
        Access_token=json.loads(user.data.decode())['access_token']
        res= self.client().post(
            '/questions/',
            headers=dict(Authorization="Bearer "+Access_token),
            data= self.question
        )
        self.assertEqual(res.status_code, 201)

        res2= self.client().get(
            '/questions/',
            headers=dict(Authorization="Bearer "+Access_token)
        )
        self.assertEqual(res2.status_code, 200)
        self.assertIn('what is 5000', str(res2.data))
    def test_question_can_get_by_id(self):
        """Test the API can read by a specific id a questions"""
        self.register_user()
        user= self.login_user()
        Access_token=json.loads(user.data.decode())['access_token']
        res= self.client().post(
            '/questions/',
            headers=dict(Authorization="Bearer "+Access_token),
            data= self.question
        )
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        res2= self.client().get(
            '/questions/{}'.format(results["id"]),
            headers=dict(Authorization="Bearer "+Access_token)
        )
        self.assertEqual(res2.status_code, 200)
        self.assertIn('what is 5000', str(res2.data))


    def test_question_can_be_edited(self):
        """Test the API can read by a specific id a questions"""
        self.register_user()
        user= self.login_user()
        Access_token=json.loads(user.data.decode())['access_token']
        res= self.client().post(
            '/questions/',
            headers=dict(Authorization="Bearer "+Access_token),
            data= self.question
        )
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        res2= self.client().put(
            '/questions/{}'.format(results["id"]),
            headers=dict(Authorization="Bearer "+Access_token),
            data={
                "question": "what is 33+20?",
                "answer": "53",
            }
        )
        self.assertEqual(res2.status_code, 200)
       
        results2 = self.client().get(
            '/questions/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " +Access_token)
        )
        #should likely break into about 5 tests for checking if it only changes 1 though all 3 values 
        #also should actuly parse json response.
        self.assertIn('what is 33+20?', str(results2.data))
        self.assertIn('53', str(results2.data))
        self.assertIn('11540003,45892053', str(results2.data))

    def test_question_can_be_deleted(self):
        self.register_user()
        user= self.login_user()
        Access_token=json.loads(user.data.decode())['access_token']
        res= self.client().post(
            '/questions/',
            headers=dict(Authorization="Bearer "+Access_token),
            data= self.question
        )
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res= self.client().delete(
            '/questions/{}'.format(results['id']),
            headers=dict(Authorization="Bearer "+Access_token)
        )
        self.assertEqual(res.status_code, 200)
        results2 = self.client().get(
            '/questions/1',
            headers=dict(Authorization="Bearer " +Access_token)
        )
        self.assertEqual(results2.status_code, 404)

if __name__ =="__main__":
    unittest.main()