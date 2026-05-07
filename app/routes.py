import json
from flask import Blueprint, jsonify, request
from app.plaid_client import client

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


@fxdxp.route("/api/create_link_token", methods=["POST"])
def create_link_token():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Parsing Failed"}), 400
    
    client_user_id = data.get("client_user_id", "sandbox-user")
    
    link_token_params = {
        "user": {
            "client_user_id": client_user_id
        },
        "client_name": "FXDXP",
        "products": ["transactions"],
        "country_codes": ["US"],
        "language": "en"
    }

    try:
        response = client.link_token_create(link_token_params)
        link_token = response["link_token"]
        return jsonify({"link_token": link_token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500