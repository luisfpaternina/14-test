# -*- coding: utf-8 -*-
# (C) 2020 Smile (<http://www.smile.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Sale Order Product Quantity Multiplier",
    "version": "0.1",
    "sequence": 100,
    "category": "Nybble",
    "author": "Nybble",
    "license": 'LGPL-3',
    "description": """
""",
    "depends": [
        'product_website_qty_ts',
        'sale',
        'sale_order_sap_state',
    ],
    "data": [
        'views/sale_order_view.xml',
        'views/sale_order_type_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
