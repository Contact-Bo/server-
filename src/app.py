import sys
from flask import Flask, render_template
from routes.users import users_blueprint


app = Flask(
    __name__,
)


@app.route("/")
def index():
    return "Hello"


app.register_blueprint(users_blueprint, url_prefix="/api/users")

if __name__ == "__main__":
    use_debug = "--debug" in sys.argv
    app.run(port=5000, debug=use_debug)
