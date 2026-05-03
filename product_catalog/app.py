from flask import Flask, jsonify

app = Flask(__name__)

products = {
    1: {"id": 1, "name": "Laptop", "price": 999.99, "stock": 5},
    2: {"id": 2, "name": "Mouse", "price": 29.99, "stock": 50},
    3: {"id": 3, "name": "Teclado", "price": 79.99, "stock": 20},
    4: {"id": 4, "name": "Monitor", "price": 299.99, "stock": 10},
}


@app.route("/products", methods=["GET"])
def list_products():
    """List all available products"""
    return jsonify(list(products.values()))


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get product details by ID"""
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
