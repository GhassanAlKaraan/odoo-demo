{
    'name': 'Test BTCO',
    'version': '1.0',
    'summary': 'Test BTCO',
    'sequence': 10,
    'description': """Test BTCO""",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base'],
    'data':[
        'security/ir.model.access.csv',
        'wizards/test_wizard_views.xml',
        'views/btco_test_views.xml',
        'data/test_model_data.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    # 'post_init_hook': '_my_custom_post_method',
    # 'pre_init_hook': '_my_custom_pre_method',
    # 'uninstall_hook': '_my_custom_uninstall_method',
}