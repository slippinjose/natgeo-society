from flask_script import Manager
from datetime import datetime

from app import create_app

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



if __name__ == "__main__":
    cli()