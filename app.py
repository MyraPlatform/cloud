from flask import Flask, request, jsonify, send_file, Response
import os
import hashlib

app = Flask(__name__)

# Directory where user data is stored
BASE_DIR = "users"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/register-user", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"error": "Missing username, password, or email"}), 400

    user_path = os.path.join(BASE_DIR, username)
    games_path = os.path.join(user_path, "games")

    if os.path.exists(user_path):
        return jsonify({"error": "User already exists"}), 409

    try:
        os.makedirs(games_path, exist_ok=True)
        with open(os.path.join(user_path, "username.txt"), "w") as f:
            f.write(username)
        with open(os.path.join(user_path, "email.txt"), "w") as f:
            f.write(email)
        with open(os.path.join(user_path, "password.hash"), "w") as f:
            f.write(hash_password(password))

        return jsonify({"status": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@app.route("/content", methods=["GET"])
def get_content():
    username = request.args.get("user")
    filepath = request.args.get("file")

    if not username or not filepath:
        return jsonify({"error": "Missing user or file parameter"}), 400

    full_path = os.path.join(BASE_DIR, username, filepath)

    if not os.path.isfile(full_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(full_path, "r") as f:
            content = f.read()
        return Response(content, mimetype="text/plain")
    except Exception as e:
        return jsonify({"error": f"Could not read file: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def homepage():
    return """<!DOCTYPE html>
<html>
  <head>
    <title>☁️ Myra Cloud</title>
  </head>
  <body>
    🌍 Myra Cloud API is running...
  </body>
</html>""", 200

if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
