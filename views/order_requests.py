import sqlite3
import json
from models import Order, Metal, Style, Size
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
            o.timestamp,
            o.size_id,
            o.style_id,
            o.metal_id,
            m.id metals_id,
            m.metal metals_metal,
            m.price metals_price,
            st.id styles_id,
            st.style styles_style,
            st.price styles_price,
            si.id sizes_id,
            si.carets sizes_carets,
            si.price sizes_price
        FROM `Orders` o
        JOIN Metals m ON m.id = o.metal_id
        JOIN Styles st ON st.id = o.style_id
        JOIN Sizes si ON si.id = o.size_id
        """)

        orders = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            order = Order(row['id'], row['timestamp'], row['size_id'],
                            row['style_id'], row['metal_id'])
            
            metal = Metal(row['metals_id'], row['metals_metal'], row['metals_price'])

            style = Style(row['styles_id'], row['styles_style'], row['styles_price'])

            size = Size(row['sizes_id'], row['sizes_carets'], row['sizes_price'])

            order.metal = metal.__dict__

            order.style = style.__dict__

            order.size = size.__dict__
        
            orders.append(order.__dict__)

    return orders

# Function with a single parameter
# def get_single_order(id):
#     # Variable to hold the found order, if it exists
#     requested_order = None

#     # Iterate the ORDERS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for order in ORDERS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if order["id"] == id:
#             requested_order = order

#             if "metalId" in requested_order:
#                 matching_metal = get_single_metal(requested_order["metalId"])
#                 requested_order["metal"] = matching_metal
#                 requested_order.pop("metalId")
#             else:
#                 ""

#             if "styleId" in requested_order:
#                 matching_style = get_single_style(requested_order["styleId"])
#                 requested_order["style"] = matching_style
#                 requested_order.pop("styleId")
#             else:
#                 ""

#             if "sizeId" in requested_order:
#                 matching_size = get_single_size(requested_order["sizeId"])
#                 requested_order["size"] = matching_size
#                 requested_order.pop("sizeId")
#             else:
#                 ""

#     return requested_order

def get_single_order(id):
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
        WHERE o.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        order = Order(data['id'], data['metal_id'], data['size_id'],
                            data['style_id'], data['timestamp'])

        return order.__dict__

# def create_order(order):
#     # Get the id value of the last order in the list
#     max_id = ORDERS[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the order dictionary
#     order["id"] = new_id

#     # Add the order dictionary to the list
#     ORDERS.append(order)

#     # Return the dictionary with `id` property added
#     return order

def create_order(new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id, timestamp )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_order['metalId'], new_order['sizeId'],
              new_order['styleId'], new_order['timestamp'], ))

        id = db_cursor.lastrowid

        new_order['id'] = id

    return new_order

# def delete_order(id):
#     # Initial -1 value for order index, in case one isn't found
#     order_index = -1

#     # Iterate the ORDERS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, order in enumerate(ORDERS):
#         if order["id"] == id:
#             # Found the order. Store the current index.
#             order_index = index

#     # If the order was found, use pop(int) to remove it from list
#     if order_index >= 0:
#         ORDERS.pop(order_index)

def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Orders
        WHERE id = ?
        """, (id, ))
    
def update_order(id, new_order):
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break