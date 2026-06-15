VALIDATION_RULES = [

    {
        "rule_name": "mandatory_product_id",
        "column": "product_id",
        "rule_type": "mandatory",
        "error_message":
            "Product ID is mandatory"
    },

    {
        "rule_name": "mandatory_order_id",
        "column": "order_id",
        "rule_type": "mandatory",
        "error_message":
            "Order ID is mandatory"
    },

    {
        "rule_name": "quantity_positive",
        "column": "quantity",
        "rule_type": "positive",
        "error_message":
            "Quantity must be greater than zero"
    },

    {
        "rule_name": "unit_price_positive",
        "column": "unit_price",
        "rule_type": "positive",
        "error_message":
            "Unit price must be greater than zero"
    },

    {
    "rule_name": "sale_date_valid",
    "column": "sale_date",
    "rule_type": "date",
    "error_message":
        "Invalid sale date"
},

    {
    "rule_name": "duplicate_order",
    "column": "order_id",
    "rule_type": "duplicate",
    "error_message":
        "Duplicate order_id found"
},

    
]