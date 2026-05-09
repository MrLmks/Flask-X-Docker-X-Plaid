import json
from flask import Blueprint, jsonify, request, render_template
from app.plaid_client import client
from datetime import date
from sqlalchemy import func, select
from utils import mapping_logos


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
        response = client.item_public_token_exchange({"public_token": public_token})
        client_user_id = data.get("client_user_id", "sandbox-user")
        from app.models import Token
        from app import db
        token_obj = Token(access_token=response["access_token"], item_id=response["item_id"], client_user_id=client_user_id)
        db.session.add(token_obj)
        db.session.commit()
        return jsonify({"status": "success", "item_id": token_obj.item_id}), 201


    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fxdxp.route("/dashboard")
def dashboard():
    from app.models import Transaction
    from app import db
    transactions = Transaction.query.all()

    query = (
        select(
            Transaction.category,
            func.sum(Transaction.amount).label("total_spent")
        ).group_by(Transaction.category)
    )
    results = db.session.execute(query).all()

    unpacked_categories = [c[0] for c in results]
    unpacked_amounts = [a[1] for a in results]
    return render_template("dashboard.html", transactions=transactions, category=unpacked_categories, amount=unpacked_amounts)


@fxdxp.route("/api/fetch_transaction", methods=["GET"])
def fetch_transaction():
    from app.models import Token, Transaction
    from app import db
    token_obj = Token.query.filter_by(client_user_id="sandbox-user").first()
    if token_obj is  None:
        return jsonify({"status": "Error : token_obj is NULL"})
    transaction_params = {
        "access_token": token_obj.access_token,
        "start_date": "2020-01-01", # To see the history of transaction logs in sandbox mode
        "end_date": date.today().isoformat()
    }
    response = client.transactions_get(transaction_params)
    transactions = response["transactions"]

    for transaction in transactions:
        existing_transaction = Transaction.query.filter_by(transaction_id=transaction["transaction_id"]).first()
        if existing_transaction is None:
            transaction_obj = Transaction(transaction_id=transaction.get("transaction_id", "Unknown"), amount=transaction["amount"], 
                                        date=transaction["date"], billing_entity=(transaction.get("merchant_name") or "Unknown"), 
                                        category=(transaction.get("category") or ["Uncategorized"][0]), currency=transaction["iso_currency_code"])
            db.session.add(transaction_obj)
    db.session.commit()
    return jsonify({"status": "success", "count": len(transactions)}), 201


@fxdxp.route("/balance", methods=["GET"])
def show_balance():
    from app.models import Transaction
    from app import db
    query = (
        select(
            Transaction.billing_entity,
            func.sum(Transaction.amount).label("spent-at")
        ).group_by(Transaction.billing_entity)
    )
    results = db.session.execute(query).all()
    transactions_sum = sum(t[1] for t in results)
    transactions = Transaction.query.all()
    logo = {}

    for t in transactions:
        logo[t.billing_entity] = mapping_logos(t.billing_entity)

    return render_template("balance.html", total=transactions_sum, logo=logo, transactions=transactions)