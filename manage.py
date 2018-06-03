from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app, db
import os
from config import Config, DevelopmentConfig, StagingConfig, DevelopmentConfig

app.config.from_object(DevelopmentConfig)
# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)



# Add the flask migrate
manager.add_command('db', MigrateCommand)

# Run the manager
if __name__ == '__main__':
    manager.run()
