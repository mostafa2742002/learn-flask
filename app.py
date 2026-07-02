from flask import Flask
from ticket_routes import ticket_bp
from database import init_database

app = Flask(__name__)

app.secret_key = "dev-secret-key"

init_database()

app.register_blueprint(ticket_bp)

if __name__ == "__main__":
    app.run(debug=True)