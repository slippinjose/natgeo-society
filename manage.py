from flask_script import Manager
from datetime import datetime

from app import create_app

import csv
import json
import logging
import click
import os
import sys
import unittest
import flask

from flask.cli import FlaskGroup


def create_cli_app(_info):
    from app import create_app
    app_env = os.environ.get('APP_ENV', 'development')
    return create_app(app_env)


@click.group(cls=FlaskGroup, create_app=create_cli_app)
@click.option('--debug', is_flag=True, default=False)
def cli(debug):
    if debug:
        os.environ['FLASK_DEBUG'] = '1'


@cli.command()
def list_routes():
    from scribe import create_app
    app_env = os.environ.get('APP_ENV', 'development')
    app = create_app(app_env)
    for l in app.url_map.iter_rules():
        print(l)


@cli.command(with_appcontext=True)
def shell():
    """Runs a shell in the app context.
    Runs an interactive Python shell in the context of a given
    Flask application. The application will populate the default
    namespace of this shell according to it's configuration.
    This is useful for executing small snippets of management code
    without having to manually configuring the application.
    """
    import IPython
    from IPython.terminal.ipapp import load_default_config
    from traitlets.config.loader import Config
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    if 'IPYTHON_CONFIG' in app.config:
        config = Config(app.config['IPYTHON_CONFIG'])
    else:
        config = load_default_config()

    config.TerminalInteractiveShell.banner1 = 'Python %s on %s\nIPython: %s\nApp: %s%s\nInstance: %s' % (
        sys.version, sys.platform, IPython.__version__, app.import_name, app.debug and ' [debug]' or '',
        app.instance_path)

    IPython.start_ipython(argv=[], config=config)


@cli.command()
@click.option('--failfast', required=False)
@click.argument('test_path', required=False)
def test(test_path, failfast=False):
    test_loader = unittest.TestLoader()
    if test_path is not None:
        tests = test_loader.loadTestsFromName(test_path)
    else:
        tests = test_loader.discover(start_dir='.', pattern='test_*.py')

    result = unittest.TextTestRunner(verbosity=2, failfast=failfast).run(tests)
    sys.exit(not result.wasSuccessful())


@cli.command()
def create_tables():
    from app.database import create_tables
    create_tables()


@cli.command()
def drop_tables():
    from app.database import drop_tables
    drop_tables()


@cli.command()
def populate_unbabelites():
    from app.handlers.unbabelites_handler import UnbabelitesHandler
    from app.database import drop_tables, create_tables

    UnbabelitesHandler.populate_unbabelites()

@cli.command()
def redo_coordinates():
    from app.handlers.unbabelites_handler import UnbabelitesHandler

    UnbabelitesHandler.redo_coordinates()


@cli.command()
def redo_from_excel():
    from app.models import Unbabelite
    from app.services.unbabelites import BulkCreateUnbabelitesService
    excel_filename = 'natgeo.csv'
    unbabelites = []

    with open(excel_filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = _get_name(row['Last name, First name'])
            except:
                print(f"Couldn't get this person's name: {row['Last name, First name']}")
                name = "John Doe"
            unbabelite = {
                "name": name,
                "country": row['Country'],
                "city": row['City of Origin']
            }
            unbabelites.append(Unbabelite(**unbabelite))

    BulkCreateUnbabelitesService(unbabelites).call()


@cli.command()
def fill_in_position_and_team():
    from app.finders import UnbabeliteFinder
    from app.services.unbabelites import UpdateUnbabeliteProfileService
    filename = 'natgeo.json'

    with open(filename) as json_file:
        data = json.load(json_file)
        for employee in data['employees']:
            name = _get_name(employee['fullName2'])
            unbabelite = UnbabeliteFinder.get_from_name(name)
            
            if not unbabelite:
                print(f"Couldn't find {name}")
            else:
                UpdateUnbabeliteProfileService(unbabelite, position=employee.get('jobTitle'), team=employee.get('customTribe')).call()
                print(f"Position and team for {unbabelite.name}: {unbabelite.position}, {unbabelite.team}")


def _get_name(name):
    last_name, first_name = name.split(', ')
    
    return f"{first_name} {last_name}"


if __name__ == "__main__":
    cli()