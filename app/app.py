import os
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

from db import init_app, get_db

load_dotenv()

app = Flask(__name__)
init_app(app)


@app.route("/getTable", methods=["GET"])
def get_tables():
    cursor = get_db().cursor()
    try:
        cursor.execute("SHOW TABLES;")
        table_names = [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()
    return jsonify({"tables": table_names}), 200


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    """Liveness: el proceso está vivo. No toca la BD."""
    return jsonify({"status": "ok"}), 200

@app.route("/ready")
def ready():
    """Readiness: la app puede atender peticiones (la BD responde)."""
    try:
        cursor = get_db().cursor()
        try:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        finally:
            cursor.close()
        return jsonify({"status": "ready", "database": "up"}), 200
    except Exception:
        app.logger.exception("Readiness check failed")
        return jsonify({"status": "not ready", "database": "down"}), 503


version_value = os.environ.get("APP_VERSION", "unknown")


@app.route("/version")
def get_version():
    return jsonify({"version": version_value}), 200