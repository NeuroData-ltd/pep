# -*- encoding: utf-8 -*-
from flask_migrate import Migrate
from flask_minify  import Minify
from sys import exit

from src.config import config_dict
from src import create_app, db

# The configuration
try:
    # Load the configuration using the default values
    app_config = config_dict["Production"]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)
Minify(app=app, html=True, js=False, cssless=False)

if __name__ == "__main__":
    app.run()
