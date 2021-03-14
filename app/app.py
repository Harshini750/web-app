from flask import Flask

from config import Config
from extensions import bcrypt, db, login_manager, migrate
from models.user import User
from views.appview import appview
from views.authview import authview


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Extensions
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Views
    app.register_blueprint(appview)
    app.register_blueprint(authview)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = "authview.login_page"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=Config.PORT)
