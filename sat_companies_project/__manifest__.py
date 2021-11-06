{
    'name': 'SAT COMPANIES PROJECT',

    'version': '14.0.1',

    'author': "Process Control",

    'contributors': ['Luis Felipe Paternina'],

    'website': "https://www.processcontrol.es/",

    'category': 'Project',

    'depends': [

        'sale_management',
        'project',
        'industry_fsm',
        'sat_companies_stock',
        'sat_companies_industry',
        'base_automation',

    ],

    'data': [
       
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_type.xml',
        'views/res_partner.xml',
        'views/project_task.xml',
        'views/sale_order.xml',
        'wizard/wizard_sale_order_type_view.xml',
        'data/project_template_inspection_notice.xml',
        
    ],
    'installable': True
}

