from flask import Flask, jsonify, request

app = Flask(__name__)

carts = {}

@app.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    """Get cart items for a user"""
    cart = carts.get(user_id, [])
    total = sum(item["price"] * item["quantity"] for item in cart)
    return jsonify({"user_id": user_id, "items": cart, "total": total})

@app.route("/cart/<int:user_id>/add", methods=["POST"])
def add_to_cart(user_id):
    """Add item to cart"""
    data = request.json
    product_id = data.get("product_id")
    product_name = data.get("product_name")
    price = data.get("price")
    quantity = data.get("quantity", 1)

    if not carts.get(user_id):
        carts[user_id] = []

    for item in carts[user_id]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            return jsonify({"message": "Item updated in cart"}), 200

    carts[user_id].append({
        "product_id": product_id,
        "product_name": product_name,
        "price": price,
        "quantity": quantity
    })

    return jsonify({"message": "Item added to cart"}), 201


if __name__ == "__main__":
    app.run(port=5002, debug=True)
