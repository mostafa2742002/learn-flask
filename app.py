from flask import Flask, render_template
from ticket_routes import ticket_bp
from database import init_database

app = Flask(__name__)

app.secret_key = "dev-secret-key"

init_database()

app.register_blueprint(ticket_bp)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)