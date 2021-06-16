from flask_script import Manager, prompt_bool
# from flask_migrate import Migrate, MigrateCommand
from school_api.app import create_app
from school_api.db import create_tables, drop_tables
from school_api.data_generator import test_db
"""
Refused flask_migration because it was overkill for this project
"""
app = create_app()

# migrate = Migrate(app, db)
manager = Manager(app)

# manager.add_command('db', MigrateCommand)


@manager.command
def createtables():
    drop_tables(app)
    create_tables(app)


@manager.command
def testdb():
    drop_tables(app)
    create_tables(app)
    test_db(app)


@manager.command
def droptables():
    if prompt_bool("Are you sure you want to lose all your data"):
        drop_tables(app)


if __name__ == '__main__':
    manager.run()
