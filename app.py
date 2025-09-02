from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from routes import auth_bp  # import your blueprint
from config import Config   # make sure Config has JWT_SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Optional: simple route to test live server
@app.route("/")
def home():
    return "Flask backend is live!"

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
