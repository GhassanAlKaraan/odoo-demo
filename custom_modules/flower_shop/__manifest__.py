{
    'name': "Sally's Flower Shop",
    'version': '1.0',
    'summary': 'FLOWER SHOP',
    'sequence': 9,
    'description': 'FLOWER SHOP',
    'category': 'Inventory/Inventory',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'product', 'sale', 'stock', ],  # sale --> product --> product variant
    'data': [
        'security/ir.model.access.csv',
        'views/flower_shop_views.xml',
        'views/product_views.xml',
        'views/stock_lot_views.xml',
        # 'views/website_sale_flower_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
