{
    'name': 'First APP',                 # الاسم الذي سيظهر في Odoo
    'version': '17.0.0.1.0',             # Odoo Version
    'author': 'Mostafa Fawzy',           # Developer Name
    'category': '',                      # التصنيف (مثل Sales, Accounting, etc.)
    'summary': '',                       # وصف قصير للموديول
    'depends': ['base', 'mail', 'base_automation', 'contacts','sale_management', 'purchase', 'stock', 'account'],   # الموديولات الأخرى التي يعتمد عليها
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/base_menu.xml',
        'views/staff.xml',
        'views/manager.xml',
        'views/project.xml',
        'reports/project_report.xml',
        'views/sales_order.xml',
    ],
    'assets': {
                'web.assets_backend': ['first_app/static/src/index.css']
    },
    'installable': True,                 # هل يمكن تثبيته؟
    'application': True,                 # هل يظهر كـ "تطبيق" رئيسي في القائمة؟
}