from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta


class User(db.Model):
    """Maps to users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
   
    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

class Question(db.Model):

    __tablename__ = 'questions'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    answer =db.Column(db.String(255))
    distractor =db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer)#, db.ForeignKey(User.id))

    def __init__(self, question,answer,distractor, created_by):
        self.question = question
        self.answer = answer
        self.distractor = distractor
        self.created_by = created_by

    def save(self):
        """Save a question.
        This applies for both creating a new question
        and updating an existing onupdate
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """This method gets all the questions for a given user."""
        return Question.query.filter_by(created_by=user_id)
        #Question.query.filter_by(created_by=user_id)

    def delete(self):
        """Deletes a given question."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of a question instance."""
        return "<Question: {}>".format(self.question,self.answer,self.distractor)
