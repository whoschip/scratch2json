from flask import Flask
from .routes import backend_bp

app = Flask(__name__)
app.register_blueprint(backend_bp, url_prefix='/api')

@app.route("/")
def home():
    return {"msg": "welcome, api goin brrrrr rn"}

if __name__ == "__main__":
    app.run(debug=True)
