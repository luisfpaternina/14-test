{
    'name': 'Partner extended',

    'version': '14.0.0.0',

    'author': "Coondev SAS",

    'contributors': ['Luis Felipe Paternina'],

    'website': "www.coodev.co",

    'category': 'partner',

    'depends': [

        'contacts',
        'base_address_city',
    ],

    'data': [

    'security/security.xml',
    'security/ir.model.access.csv',
    'views/res_partner.xml',
    'views/res_partner_address.xml',
    'views/res_partner_address_cardinals.xml',
    'views/res_partner_city.xml',
                   
    ],
    'installable': True
}

