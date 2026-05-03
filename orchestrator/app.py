from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

PRODUCT_CATALOG_URL = "http://localhost:5001"
SHOPPING_CART_URL = "http://localhost:5002"


@app.route("/", methods=["GET"])
def home():
    """Get all available products from catalog"""
    try:
        response = requests.get(f"{PRODUCT_CATALOG_URL}/products")
        products = response.json()
        return jsonify({"message": "Welcome to E-Commerce", "products": products})
    except Exception as e:
        return jsonify({"error": f"Could not fetch products: {str(e)}"}), 500


@app.route("/cart/<int:user_id>", methods=["GET"])
def view_cart(user_id):
    """View user's shopping cart"""
    try:
        response = requests.get(f"{SHOPPING_CART_URL}/cart/{user_id}")
        cart = response.json()
        return jsonify(cart)
    except Exception as e:
        return jsonify({"error": f"Could not fetch cart: {str(e)}"}), 500


@app.route("/order", methods=["POST"])
def create_order():
    """Create an order: add product to cart and return order summary"""
    data = request.json
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"error": "user_id and product_id are required"}), 400

    try:
        product_response = requests.get(
            f"{PRODUCT_CATALOG_URL}/products/{product_id}"
        )
        if product_response.status_code != 200:
            return jsonify({"error": "Product not found"}), 404

        product = product_response.json()

        cart_payload = {
            "product_id": product["id"],
            "product_name": product["name"],
            "price": product["price"],
            "quantity": data.get("quantity", 1)
        }
        cart_response = requests.post(
            f"{SHOPPING_CART_URL}/cart/{user_id}/add",
            json=cart_payload
        )

        if cart_response.status_code != 201:
            return jsonify({"error": "Failed to add item to cart"}), 500

        cart_response = requests.get(f"{SHOPPING_CART_URL}/cart/{user_id}")
        cart = cart_response.json()

        return jsonify({
            "message": "Order created successfully",
            "user_id": user_id,
            "product": product,
            "cart": cart
        }), 201

    except Exception as e:
        return jsonify({"error": f"Order creation failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
