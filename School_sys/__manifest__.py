{
    'name': 'School Management System',
    'version': '1.0.1',
    'summary': 'Full School Management: Students, Teachers, Grades, Attendance, Reports',
    'description': """
        Complete School Management System for Odoo 17
        =============================================
        Features:
        - Student & Teacher Management
        - Class & Subject Management
        - Attendance Tracking
        - Exam & Grade Management
        - Fee Management
        - Internal & External API
        - QWeb Reports
        - Wizards
        - Dashboards
        - Role-based Security
    """,
    'author': 'Mostafa Fawzy',
    'category': '',
    'depends': ['base', 'mail', 'web'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/school_security.xml',

        # Data
        'data/sequence_data.xml',

        # Wizards
        'wizards/attendance_wizard_views.xml',
        'wizards/grade_report_wizard_views.xml',

        # Views
        'views/student_views.xml',
        'views/teacher_views.xml',
        'views/classroom_views.xml',
        'views/subject_views.xml',
        'views/attendance_views.xml',
        'views/exam_views.xml',
        'views/fee_views.xml',
        # 'views/dashboard_views.xml',
        'views/menu_views.xml',
        # 'views/res_config_settings_views.xml',


        # Reports
        'reports/student_report.xml',
        'reports/grade_report.xml',
        'reports/attendance_report.xml',
        'reports/fee_report.xml',

    ],
    # 'assets': {
    #         'web.assets_backend': [
    #             'school_sys/static/src/css/school_dashboard.css',
    #             'school_sys/static/src/js/school_dashboard.js',
    #         ],
    #     },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
