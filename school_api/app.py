from flask import Flask, redirect
from .config import config_by_name, basedir
from flasgger import Swagger
import os


def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    from .models import db
    db.init_app(app)

    from .resources.v1.api import api_bp as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    @app.route('/')
    def redirect_to_apidocs():
        return redirect("/apidocs", code=302)

    swag = Swagger(app,
                   template_file=os.path.join(basedir, 'docs', 'template.yaml'))

    return app
