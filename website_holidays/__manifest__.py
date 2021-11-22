###############################################################################################
#
# Luis Felipe Paternina
# Ing.Sistemas                                
# Odoo Dev
#
# E-mail: lfpaternina93@gmail.com 
# Cel: +573215062353
#
# Bogotá,Colombia
#
#
###############################################################################################

{
    'name': 'website holidays',

    'version': '14.0.0.0',

    'author': "Luis Felipe Paternina",

    'contributors': ['Luis Felipe Paternina'],

    'website': "",

    'category': 'holidays',

    'depends': [

        'hr_holidays',
        'hr',
        'contacts',
        'base',
    ],

    'data': [
       
        
        'views/website_form.xml',
                    
    ],
    'installable': True
}

