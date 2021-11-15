# -*- coding: utf-8 -*-
# (C) 2020 Smile (<http://www.smile.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Sale Order SAP States",
    "version": "0.1",
    "sequence": 100,
    "category": "Nybble",
    "author": "Nybble",
    "license": 'LGPL-3',
    "description": """
Este módulo agrega los estados de sap a la orden de venta""",
    "depends": [
        'base','sale_stock_ux', 'sale','libus_argul_b2b'
    ],
    "data": [
        'views/sale_order_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
