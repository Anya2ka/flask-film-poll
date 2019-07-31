from flask import Flask
from src.server import api

import src.views.movies  # noqa
import src.views.polls  # noqa

app = Flask(__name__)
api.init_app(app)
