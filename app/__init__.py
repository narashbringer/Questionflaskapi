import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from app.config import BaseConfig,ProductionConfig
from flask import request, jsonify, abort, make_response

db = SQLAlchemy()

# def create_app(config_name):
from app.models import User,Question
app = FlaskAPI(__name__, static_folder=None)
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
    )
app.config.from_object(app_settings)
    #app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.route('/questions/', methods=['POST', 'GET'])
def question():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    question = str(request.data.get('question', ''))
                    answer = str(request.data.get('answer', ''))
                    distractor = str(request.data.get('distractor', ''))
                    if (question and answer and distractor):
                        question = Question(question=question,
                            answer=answer,
                            distractor=distractor,
                            created_by=user_id)

                        question.save()

                        response = jsonify({
                            'id': question.id,
                            'question': question.question,
                            'answer':question.answer,
                            'distractor':question.distractor,
                            'date_created': question.date_created,
                            'date_modified': question.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all the questions created by this user
                    questions = Question.query.filter_by(created_by=user_id)
                    questions2 = Question.query.filter_by(created_by=None)
                    results = []

                    for question in questions:
                        obj = {
                            'id': question.id,
                            'question': question.question,
                            'answer':question.answer,
                            'distractor':question.distractor,
                            'date_created': question.date_created,
                            'date_modified': question.date_modified,
                            'created_by': question.created_by
                        }
                        results.append(obj)
                    for question in questions2:
                        obj = {
                            'id': question.id,
                            'question': question.question,
                            'answer':question.answer,
                            'distractor':question.distractor,
                            'date_created': question.date_created,
                            'date_modified': question.date_modified,
                            'created_by': question.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

@app.route('/questions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def question_manipulation(id, **kwargs):
     # retrieve a question using it's ID
            question = Question.query.filter_by(id=id).first()
            if not question:
            # Raise an HTTPException with a 404 not found status code
                abort(404)

            if request.method == 'DELETE':
                question.delete()
                return {
                "message": "question {} deleted successfully".format(question.id) 
                }, 200

            elif request.method == 'PUT':
                questions = str(request.data.get('question', ''))
                answers = str(request.data.get('answer', ''))
                distractors = str(request.data.get('distractor', ''))

                if questions is not "":
                    question.question = questions

                if answers  is not "":
                    question.answer=answers
                
                if distractors  is not "":
                    question.distractor=distractors
                    
                question.save()
                response = jsonify({
                            'id': question.id,
                            'question': question.question,
                            'answer':question.answer,
                            'distractor':question.distractor,
                            'date_created': question.date_created,
                            'date_modified': question.date_modified,
                            'created_by': question.created_by
                        })
                response.status_code = 200
                return response
            else:
            # GET
                response = jsonify({
                     'id': question.id,
                     'question': question.question,
                     'answer':question.answer,
                     'distractor':question.distractor,
                     'date_created': question.date_created,
                     'date_modified': question.date_modified,
                })
                response.status_code = 200
                return response



from .auth import auth_blueprint
app.register_blueprint(auth_blueprint)
    
    