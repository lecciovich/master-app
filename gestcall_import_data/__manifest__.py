# -*- coding: utf-8 -*-
{
    'name' : 'Gestcall Import Data',
    'version' : '1.12.0',
    'summary': 'Gestcall Import Data',
    'description': """
            This module allows you to import data from excel file .

    """,
    'category': 'Management',
    'author': 'Boubaker Abdallah',
    'website': '',
    'images' : [],
    'depends' : ['web','base','mail'],
    'css':[ ],

    'data': [
        'security/ir.model.access.csv',
        'views/import_data_view.xml',

    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
