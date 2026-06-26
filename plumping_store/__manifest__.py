{
    'name': 'Plumping Store Managment',  # الاسم الذي سيظهر في Odoo
    'version': '17.0.1.0',               # Odoo Version
    'author': 'Mostafa Fawzy',           # Developer Name
    'category': '',                      # التصنيف (مثل Sales, Accounting, etc.)
    'summary': '',                       # وصف قصير للموديول
    'depends': ['base', 'sale_management', 'purchase', 'stock'],   # الموديولات الأخرى التي يعتمد عليها
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard.xml',
        'views/menu_view.xml',
        'data/sequence.xml',
        'data/data.xml',
        'views/product_view_inherit.xml',
        'wizards/quick_sale_order_wizard_view.xml',
        'reports/Product_report.xml',
        'views/sales_order_view_inherit.xml',
    ],
    'assets': {
                'web.assets_backend': [
                    'plumping_store/static/src/css/style.css',
                    'plumping_store/static/src/components/listView/listView.js',
                    'plumping_store/static/src/components/listView/listView.xml',
                    'plumping_store/static/src/components/listView/listView.css',
                    'plumping_store/static/src/components/formView/formView.js',
                    'plumping_store/static/src/components/formView/formView.xml',
                    'plumping_store/static/src/components/formView/formView.css',

                ]
    },
    'installable': True,                 # هل يمكن تثبيته؟
    'application': True,                 # هل يظهر كـ "تطبيق" رئيسي في القائمة؟
}