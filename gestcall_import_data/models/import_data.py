# -*- coding: utf-8 -*-
import sys  
import re
import datetime
import base64
from odoo import api, fields, models, _
from tempfile import TemporaryFile
import csv
import time
import functools
from xmlrpc import client
import openpyxl
import os
import xlrd
import fnmatch
import subprocess
import logging
import math
from docutils.nodes import address
logger=logging.getLogger('_______Boubaker____________')
 

class IMPORTDATA(models.Model):
   
    AVAILABLE_STATES = [
                      ('draft', 'Draft'),
                      ('failure', 'Failure'),
                       ('done', 'Done'),
                     ]
    
    _name = 'import.import'
    _inherit = ['mail.thread']  
    _description = 'Import Data' 
    _order = 'id desc' 
    
    name =  fields.Char('Nom de la pièce jointe')
    description = fields.Text('Description de fichier')
    data = fields.Binary('Fichier', required=True)
    type = fields.Selection([('lesson', 'lesson'), ('partner', 'Partner')], 'Type', required=True)
    filename = fields.Char('Nom fichier')
    state = fields.Selection(AVAILABLE_STATES, 'Etat', readonly=True, default='draft')
    path = fields.Char('Path', default='F:/')

             
    @api.multi
    def import_lesson_data(self): 
        lesson_obj = self.env['gestcal.lesson']
        partner_obj = self.env['res.partner']
        dest_filename = self.path + self.filename
        workbook = xlrd.open_workbook(dest_filename)
        for sheet in workbook.sheets():
            cols = sheet.row_values(0) 
            lesson_date = cols.index(u'date') 
            start_date = cols.index(u'start')
            end_date = cols.index(u'end')
            for rowx in range(0,sheet.nrows):
                rowx += 1 
                len_nr = len(range(sheet.nrows))
                logger.info("_len_nr______________: %s ",len_nr)
                if rowx < len_nr:
                    cols = sheet.row_values(rowx)
                    lesson_date_obj = cols[lesson_date] or ''
                    start_obj = cols[start_date] or ''
                    end_obj = cols[end_date] or ''
                    d0 = datetime.date(1900, 1, 1)
                    delta = datetime.timedelta(days=(lesson_date_obj -2))
                    date_lesson = d0 + delta
                    logger.info("_date_lesson______________: %s ",date_lesson)

                    if date_lesson:
                        lesson_id = lesson_obj.search([('date', '=', date_lesson)])
                        logger.info("_lesson_id______________: %s ",lesson_id)

                        if not lesson_id:
                            lesson_vals={
                                'date': date_lesson,
                                'start_time': start_obj * 24,
                                'end_time': end_obj * 24,
                                'teacher_id': 7,
                                }    
                            logger.info("_lesson_vals______________: %s ",lesson_vals)
                            lesson_id = lesson_obj.create(lesson_vals) 

            self.write({'state':'done'})         
        return True             
                   
                        
 
    