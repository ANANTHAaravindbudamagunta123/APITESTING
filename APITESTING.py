from flask import Flask, request, jsonify
import os
app = Flask(__name__)

# In-memory data store
items = [
    {"id": 1, "name": "Item One"},
    {"id": 2, "name": "Item Two"}
]

# GET all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# GET single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    return jsonify(item)

# POST create new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": data.get("name")
    }
    items.append(new_item)
    return jsonify(new_item), 201

# PUT update entire item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    
    data = request.get_json()
    item["name"] = data.get("name")
    return jsonify(item)

# PATCH partial update
@app.route('/items/<int:item_id>', methods=['PATCH'])
def patch_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    
    data = request.get_json()
    if "name" in data:
        item["name"] = data["name"]
    return jsonify(item)

# DELETE item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    new_list = [i for i in items if i["id"] != item_id]

    if len(new_list) == len(items):
        return jsonify({"message": "Item not found"}), 404

    items = new_list
    return jsonify({"message": "Item deleted"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


