{
    'name' : "Sally's Flower Shop",
    'version' : '1.0',
    'summary': 'FLOWER SHOP',
    'sequence': 10,
    'description': 'FLOWER SHOP',
    'category': 'Inventory/Inventory',
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/flower_shop_views.xml'
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
