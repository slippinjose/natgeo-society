from flask_script import Manager
from datetime import datetime

from app import create_app

import logging
import os
import sys
import unittest
import flask

logging.info("Starting Logger for Natgeo Society")

app_env = os.environ.get('APP_ENV', 'development')
if 'run_tests' in sys.argv:
    app_env = 'testing'
app = create_app(app_env)
manager = Manager(app)

log = logging.getLogger(__name__)


@manager.command
def run_tests():
    tests = unittest.TestLoader().discover(start_dir='.', pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1



if __name__ == "__main__":
    manager.run()