import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if not 'db' in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], 
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # To return dict() from database
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.execute(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database initialized')

def init_app():
    current_app.teardown_appcontext(close_db)
    current_app.cli.add_command(init_db_command)
        
