import unittest
from app import create_app,db
from flask_script import Manager,Server
from app.models import User,Role,Blog,Comment,Category,Subscribe
from  flask_migrate import Migrate, MigrateCommand

# Creating app instance
app = create_app('production')


migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
manager.add_command('server',Server)


@manager.command
def test():
    """Run the unittests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User,Role = Role,Blog = Blog,Comment = Comment,Category = Category,Subscribe = Subscribe)


if __name__ == '__main__':
    # app.secret_key = 'gL0711'
    manager.run()