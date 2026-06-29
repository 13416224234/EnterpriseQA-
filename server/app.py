from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)
jwt.init_app(app)

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.document import document_bp
from routes.qa import qa_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(document_bp, url_prefix="/api/document")
app.register_blueprint(qa_bp, url_prefix="/api/qa")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)