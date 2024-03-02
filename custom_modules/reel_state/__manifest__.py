{
    'name' : 'REEL STATE Management Software',
    'version' : '1.0',
    'summary': 'REEL STATE',
    'sequence': 10,
    'description': 'REEL STATE',
    'category': 'Real Estate/Real Estate',
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/reel_property_views.xml'
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
