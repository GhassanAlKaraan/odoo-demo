{
    'name': "Sally's Flower Shop",
    'version': '1.0',
    'summary': 'FLOWER SHOP',
    'sequence': 9,
    'description': 'FLOWER SHOP',
    'category': 'Inventory/Inventory',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/flower_shop_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
