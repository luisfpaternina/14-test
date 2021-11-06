{
    'name': 'SAT COMPANIES PARTNER',

    'version': '14.0.1',

    'author': "Process Control",

    'contributors': ['Luis Felipe Paternina'],

    'website': "https://www.processcontrol.es/",

    'category': 'Partner',

    'depends': [

        'contacts',
        'hr',
        'base_automation',
        'base',
    ],

    'data': [
       
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_delegation.xml',
        'views/res_partner_type.xml',
        'views/res_partner.xml',
        'views/res_partner_population.xml',
        'data/sequences.xml',
        
    ],
    'installable': True
}

