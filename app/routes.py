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


def get_json_or_400():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Parsing Failed"}), 400
    return data


@fxdxp.route("/api/create_link_token", methods=["POST"])
def create_link_token():
    data = get_json_or_400()
    
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
    
@fxdxp.route("/api/exchange_public_token", methods=["POST"])
def exchange_public_token():
    data = get_json_or_400()
    
    public_token = data.get("public_token")
    
    if public_token is None:
        return jsonify({"error": "Public token not found"}), 400
    
    try:
        response = client.item_public_token_exchange(public_token)
        client_user_id = data.get("client_user_id", "sandbox-user")
        # Against circular import
        from app.models import Token
        from app import db
        token_obj = Token(access_token=response["access_token"], item_id=response["item_id"], client_user_id=client_user_id)
        db.session.add(token_obj)
        db.session.commit()
        return jsonify({"status": "success", "item_id": token_obj.item_id}), 201


    except Exception as e:
        return jsonify({"error": str(e)}), 500
