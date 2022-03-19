from flask import Flask
from database import db
from blueprints.continuous_resource_blueprint import create_continuous_resource_blueprint
import os
import logging

logger = logging.getLogger(__name__)

def create_app(db_uri: str) -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register continuous resource blueprints
    app.register_blueprint(
        create_continuous_resource_blueprint(
            blueprint_name="InventoryBlueprint",
            resource_type="Inventory",
            resource_prefix="Inventory"
        ),
        url_prefix='/api'
    )

    app.register_blueprint(
        create_continuous_resource_blueprint(
            blueprint_name="FruitsBlueprint",
            resource_type="Fruits",
            resource_prefix="fruits"
        ),
        url_prefix='/api'
    )

    return app


if __name__=="__main__":
    app = create_app(db_uri="sqlite:///red.db")
    app.run("0.0.0.0", port=5000, debug=True)
