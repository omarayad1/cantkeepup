from flask.ext.script import Manager, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
import os
import unittest
import coverage

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
	""" Runs the tests without coverage."""
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

class TestSingle(Command):
    """ Run a single test case using '-n full.test.case.path' """
    def __init__(self, default_name=None):
        self.default_name=default_name

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
        ]

    def run(self, name):
        assert(name is not None)
        tests = unittest.TestLoader().loadTestsFromName(name)
        unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command('test_single', TestSingle)

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*',
        omit='*/__init__.py'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

@manager.command
def run():
    port = int(os.environ.get('PORT', 5000))       
    app.run(host='0.0.0.0', port=port)         

if __name__ == '__main__':
    manager.run()
