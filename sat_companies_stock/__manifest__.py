{
    'name': 'SAT COMPANIES STOCK',

    'version': '14.0.1.0',

    'author': "Process Control",

    'contributors': ['Luis Felipe Paternina'],

    'website': "https://www.processcontrol.es/",

    'category': 'stock',

    'depends': [

        'sale_management',
        'stock',
        'purchase',
        'contacts',
        'sat_companies_partner',
        'sale_subscription',
        'sat_companies_zones',

    ],

    'data': [
       
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/products.xml',
        'views/stock_gadgets.xml',
        'views/stock_gadgets_state.xml',
        'views/stock_gadgets_types_assistance.xml',
        'views/stock_gadgets_use.xml',
        'views/stock_gadgets_contract_type.xml',
        'views/stock_gadgets_billing_period.xml',
        'views/stock_gadgets_increase_type.xml',
        'views/sale_subscription.xml',
        
    ],
    'installable': True
}

