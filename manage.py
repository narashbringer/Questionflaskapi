import os
import unittest
import csv
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app #from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def importcsv(file):
        with open(file, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='|')#, quotechar='|')
            from app.models import Question
            for row in spamreader:
                question = Question(
                    question=row[0],
                    answer=row[1],
                    distractor=row[2],
                    created_by=None
                )
                question.save()
            return 0
   

if __name__ == '__main__':
    manager.run()

