{
    'name': 'TO DO APP',                 # الاسم الذي سيظهر في Odoo
    'version': '17.0',                   # Odoo Version
    'author': 'Mostafa Fawzy',           # Developer Name
    'category': '',                      # التصنيف (مثل Sales, Accounting, etc.)
    'summary': '',                       # وصف قصير للموديول
    'depends': ['base','mail'],                # الموديولات الأخرى التي يعتمد عليها
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu_view.xml',
        'views/todo_view.xml',
        'wizard/change_status_wizard_view.xml',
        'reports/todo_report.xml',
    ],
    'assets': {
        'web.assets_backend':['second_app/static/src/index.css']
    },
    'installable': True,                 # هل يمكن تثبيته؟
    'application': True,                 # هل يظهر كـ "تطبيق" رئيسي في القائمة؟
}
