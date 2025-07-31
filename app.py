
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

MENU_FILE = 'menu.json'
UPLOAD_FOLDER = os.path.join(app.static_folder, 'assets')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/menu", methods=["GET"])
def get_menu():
    if not os.path.exists(MENU_FILE):
        return jsonify([])
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/menu", methods=["POST"])
def save_menu():
    data = request.json
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"status": "ok"})

@app.route("/menu/delete", methods=["POST"])
def delete_item():
    index = request.json.get("index")
    if not os.path.exists(MENU_FILE):
        return jsonify({"status": "error", "message": "menu not found"}), 400
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if 0 <= index < len(data):
        data.pop(index)
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "message": "invalid index"}), 400

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    return jsonify({"path": f"static/assets/{filename}"})

@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/admin")
def admin():
    return send_from_directory(app.static_folder, "admin.html")

if __name__ == "__main__":
    app.run(debug=True)
