# contain the appliaction factory
# tell Python that dashboard directory should be treated as a package.

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dashboard.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import medicine
    app.register_blueprint(medicine.bp)
    app.add_url_rule('/medicine', endpoint='index')

    from . import trip
    app.register_blueprint(trip.bp)
    app.add_url_rule('/trip', endpoint='index')

    from . import takeout
    app.register_blueprint(takeout.bp)
    app.add_url_rule('/takeout', endpoint='index')

    from . import doctor
    app.register_blueprint(doctor.bp)
    app.add_url_rule('/doctor', endpoint='index')

    from . import news
    app.register_blueprint(news.bp)
    app.add_url_rule('/news', endpoint='index')

    from . import symptom
    app.register_blueprint(symptom.bp)
    app.add_url_rule('/symptom', endpoint='index')

    from . import indicator
    app.register_blueprint(indicator.bp)
    app.add_url_rule('/indicator', endpoint='index')

    return app