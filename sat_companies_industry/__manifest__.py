{
    'name': 'SAT COMPANIES INDUSTRY',

    'version': '14.0.1',

    'author': "Process Control",

    'contributors': ['Luis Felipe Paternina'],

    'website': "https://www.processcontrol.es/",

    'category': 'industry',

    'depends': [

        'maintenance',
        'industry_fsm',
        'project',
        'base_automation',
        'sat_companies_stock',

    ],

    'data': [
       
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/maintenance_minute_point.xml',
        'views/maintenance_type_deffect.xml',
        'views/project_task.xml',
        'views/project_task_ot_checklist.xml',
        'views/project_task_ot_type.xml',
        'views/project_task_type_associated.xml',
        'views/project_task_inspection.xml',
        'views/project_task_ot_checklist_location.xml',
        'reports/worksheet.xml',
        'data/sequences.xml',
        
    ],
    'installable': True
}

