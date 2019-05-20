# See LICENSE file for full copyright and licensing details.


{
    'name': 'Module for Calls activity management',
    'version': '12.0.1.0.4',
    'author': "MasterFor",
    'website': "http://www.masterfor.it",
    'license': "AGPL-3",
    'category': 'Calls activity management',
    'summary': '',
    'images': ['static/description/SchoolTimetable.png'],
    'depends': ['base','calendar','hr','contacts'],
    'data': ['security/ir.model.access.csv',
             'views/gest_call_view.xml',
             'views/res_partner.xml',
             'views/gest_call_menu.xml',
             ], 
    'installable': True,
    'application': True
}
