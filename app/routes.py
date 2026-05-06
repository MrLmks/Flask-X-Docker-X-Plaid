from flask import Blueprint, jsonify

fxdxp = Blueprint("FXDXP", __name__, template_folder="templates")

@fxdxp.route("/")
def welcome_message():
    return "Welcome to FXDXP 💳"

@fxdxp.route("/about", methods=["GET"])
def json_message():
    return jsonify(message={"status":"ok"})

@fxdxp.route("/health")
def health_check():
    return {"status": "ok"}, 200