import os

import click
import gunicorn.app.base
from flask.cli import FlaskGroup, pass_script_info

from app import app, db
from app.refbooks.Client.data_import import import_from_dir
from app.refbooks.MKB.load import load_mkb_csv

cli = FlaskGroup(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db
    }


@cli.command('import')
@click.argument('dirname')
@click.option('--limit', '-l', default=0, help='Maximum number of rows.')
def client_import(dirname, limit):
    """ Import clients from directory with dbf files. """
    if os.path.isdir(dirname):
        import_from_dir(dirname, limit)
    else:
        print(f'Incorrect path: {dirname}')


class GunicornApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, application, options=None):
        self.application = application
        self.options = options or {}
        super(GunicornApplication, self).__init__()

    def init(self, parser, opts, args):
        return self.options

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@cli.command('gunicorn', short_help='Start serving application from Gunicorn.')
@click.option('--host', '-h', default='127.0.0.1', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, help='The port to bind to.')
@click.option('--workers', '-w', default=2, help='Number of Gunicorn workers')
@pass_script_info
def run_gunicorn(info, host, port, workers):
    options = {
        'workers': workers,
        'bind': '{}:{}'.format(host, port)
    }
    flask_app = info.load_app()
    GunicornApplication(flask_app, options).run()


@cli.command('tables', short_help='Show db tables description.')
@pass_script_info
def tables_info(info):
    for table_name, table in db.metadata.tables.items():
        print(table_name + ':')
        for column in table.columns:
            com = column.comment or ''
            print(f'\t"{column.name}" ({column.type}) {com}')


@cli.command('load_mkb', short_help='Import MKB-10')
@click.argument('filename')
def load_mkb(filename):
    if os.path.isfile(filename):
        load_mkb_csv(filename)
    else:
        print(f'Incorrect path: {filename}')


if __name__ == '__main__':
    cli()
