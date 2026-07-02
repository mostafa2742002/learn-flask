from flask import Flask
from ticket_routes import ticket_bp

app = Flask(__name__)

app.register_blueprint(ticket_bp)

app.secret_key = "dev-secret-key"


if __name__ == "__main__":
    app.run(debug=True)