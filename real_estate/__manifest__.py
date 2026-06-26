{
    'name': 'Real Estate System',
    'version': '1.0',
    'summary': 'Full Real Estate: Property, Owners, Customers, Sales, Rentals and Contracts',
    'description': """
        Complete Real Estate System for Odoo 17
        =============================================
        Features:
        - Property Management
        - Owners
        - Customers
        - Sales
        - Rentals
        - Contracts
        - Internal & External API
        - QWeb Reports
        - Wizards
        - Dashboards
        - Role-based Security
    """,
    'author': 'Mostafa Fawzy',
    'category': '',
    'depends': ['base', 'mail', 'web', 'board'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/sequence_data.xml',

        # Wizards
        'wizards/quick_create_property_wizard.xml',

        # Views
        'views/dashboard_views.xml',
        'views/property_views.xml',

        'views/menu_views.xml',

        # Reports
        'reports/property_report.xml'

    ],
    'assets': {
            'web.assets_backend': [
                'real_estate/static/src/index.css',
                'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.0/chart.umd.js',
                'real_estate/static/src/components/dashboard/dashboard.js',
                'real_estate/static/src/components/dashboard/dashboard.xml',
                'real_estate/static/src/components/dashboard/dashboard.css',
            ],
        },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
