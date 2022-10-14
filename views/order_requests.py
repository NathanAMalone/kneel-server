from importlib import import_module
import sqlite3
import json
from models import Order
from .metal_requests import get_single_metal
from .style_requests import get_single_style
from .size_requests import get_single_size

ORDERS = [
        {
            "id": 1,
            "metalId": 3,
            "sizeId": 2,
            "styleId": 3,
            "timestamp": 1614659931693
        } 
    ]

# def get_all_orders():
#     return ORDERS

def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp
        FROM Orders o
        """)

        orders = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            order = Order(row['id'], row['metal_id'], row['size_id'],
                            row['style_id'], row['timestamp'],)
        
            orders.append(order.__dict__)

    return orders

# Function with a single parameter
def get_single_order(id):
    # Variable to hold the found order, if it exists
    requested_order = None

    # Iterate the ORDERS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for order in ORDERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if order["id"] == id:
            requested_order = order

            if "metalId" in requested_order:
                matching_metal = get_single_metal(requested_order["metalId"])
                requested_order["metal"] = matching_metal
                requested_order.pop("metalId")
            else:
                ""

            if "styleId" in requested_order:
                matching_style = get_single_style(requested_order["styleId"])
                requested_order["style"] = matching_style
                requested_order.pop("styleId")
            else:
                ""

            if "sizeId" in requested_order:
                matching_size = get_single_size(requested_order["sizeId"])
                requested_order["size"] = matching_size
                requested_order.pop("sizeId")
            else:
                ""

    return requested_order

def create_order(order):
    # Get the id value of the last order in the list
    max_id = ORDERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the order dictionary
    order["id"] = new_id

    # Add the order dictionary to the list
    ORDERS.append(order)

    # Return the dictionary with `id` property added
    return order

def delete_order(id):
    # Initial -1 value for order index, in case one isn't found
    order_index = -1

    # Iterate the ORDERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Store the current index.
            order_index = index

    # If the order was found, use pop(int) to remove it from list
    if order_index >= 0:
        ORDERS.pop(order_index)
    
def update_order(id, new_order):
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break