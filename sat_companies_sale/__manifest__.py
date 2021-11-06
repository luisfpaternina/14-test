{
    'name': 'SAT COMPANIES SALE',

    'version': '14.0.1',

    'author': "Process Control",

    'contributors': ['Luis Felipe Paternina'],

    'website': "https://www.processcontrol.es/",

    'category': 'Sale',

    'depends': [

        'sale_management',
        'crm',
        'sat_companies_project',
        'base_automation',
        'sale_subscription',
        'sat_companies',

    ],

    'data': [
       
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'views/crm_lead_type.xml',
        'views/sale_order.xml',
        'data/sale_order_sent_email_data.xml',
        'data/sale_order_maintenance_offer.xml',
        'data/crm_lead_opportunity_notify.xml',
        'data/base_automatization.xml',
        
    ],
    'installable': True
}

