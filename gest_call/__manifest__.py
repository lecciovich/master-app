# See LICENSE file for full copyright and licensing details.


{
    'name': 'Module for Calls activity management',
    'version': '12.0.1.0.4',
    'author': "MasterFor",
    'website': "http://www.masterfor.it",
    'license': "AGPL-3",
    'category': 'Calls activity management',
    'summary': '',
    'images': ['/home/odoovm/Odoo/odoo-12.0/master-app/gest_call/static/src/img/import.png'],
    'depends': ['base','calendar','hr','contacts','web_widget_timepicker','display_import_button'],
    'data': ['security/ir.model.access.csv',
             'views/project_view.xml',
             'views/lesson_view.xml',
             'views/plan_view.xml',
             'views/place_view.xml',
             'views/course_view.xml',
             'views/seqence_gestcall.xml',
             'views/attachment_view.xml',
             'views/res_partner.xml',
             'views/hr_employee.xml',
             'views/gest_call_menu.xml',
             ],
    'css': ['/home/odoovm/Odoo/odoo-12.0/master-app/gest_call/static/src/css/styles.css'],
    'installable': True,
    'application': True
}
