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
from odoo.exceptions import UserError,ValidationError
from tempfile import TemporaryFile
import tempfile
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
    path = fields.Char('Path', default='')

             
    @api.multi
    def import_lesson_data(self): 
        lesson_obj = self.env['gestcal.lesson']
        partner_obj = self.env['res.partner']
        project_obj = self.env['gestcal.project']
        course_obj = self.env['gestcal.course']
        place_obj = self.env['gestcal.place']
#         dest_filename = self.path + self.filename
#         workbook = xlrd.open_workbook(dest_filename)
        file_path = tempfile.gettempdir()+ self.filename
        data = self.data
        f = open(file_path,'wb')
        decode = base64.b64decode(data)
        logger.info("_decode______________: %s ",decode)
        f.write(decode)
        f.close()
        workbook = xlrd.open_workbook(file_path)
        
        for sheet in workbook.sheets():
            cols = sheet.row_values(0) 
            lesson_date = cols.index(u'date') 
            start_date = cols.index(u'start')
            end_date = cols.index(u'end')
            teacher = cols.index(u'teacher list')
            project = cols.index(u'project Id')
            project_title = cols.index(u'project title')
            course = cols.index(u'course id')
            course_title = cols.index(u'course title')
            repetition_nb = cols.index(u'repetition')
            hour_tot = cols.index(u'hours')
            place = cols.index(u'place')
            for rowx in range(0,sheet.nrows):
                rowx += 1 
                len_nr = len(range(sheet.nrows))
                logger.info("_len_nr______________: %s ",len_nr)
                if rowx < len_nr:
                    cols = sheet.row_values(rowx)
                    lesson_date_obj = cols[lesson_date] or ''
                    start_obj = (cols[start_date]) * 24 or ''
                    end_obj = (cols[end_date]) * 24 or ''
                    partner_id = cols[teacher] or ''
                    project_id = cols[project] or ''
                    project_title_s = cols[project_title] or ''
                    project_title_name = str(project_title_s)
                    course_id = cols[course] or ''
                    course_title_name = cols[course_title] or ''
                    repetition_int = cols[repetition_nb] or ''
                    repetition_nb = int(repetition_nb)
                    hour_to = cols[hour_tot] or '' 
                    place_id = cols[place] or ''
                    d0 = datetime.date(1900, 1, 1)
                    delta = datetime.timedelta(days=int(lesson_date_obj -2))
                    date_lesson = d0 + delta
                    logger.info("_date_lesson______________: %s ",date_lesson)

                    if partner_id:
                        logger.info("_partner_id______________: %s ",partner_id)
                        teacher_name = partner_obj.search([('name', '=', partner_id)])
                        if not teacher_name:
                            teacher_vals ={
                                'name': partner_id,
                                
                                }
                            teacher_name = partner_obj.create(teacher_vals)
                            logger.info("___________partner_obj_id________: %s ",teacher_name)
                    
                    if project_id:
                        logger.info("_project__id______________: %s ",project_id)
                        project_name = project_obj.search([('project_id', '=', project_id)])
                        if not project_name:
                            project_vals ={
                                'project_id': project_id,
                                'title': project_title_name,
                                }
                            logger.info("_________project_vals>________: %s ",project_vals)  
                            project_name = project_obj.create(project_vals)
                            logger.info("___________project_name_id________: %s ",project_name)                

                    if course_id:
                        logger.info("_course_id______________: %s ",course_id)
                        course_name = course_obj.search([('course_id', '=', course_id)])
                        if not course_name:
                            course_vals ={
                                'name': course_title_name,
                                'course_id': course_id,
                                'project_id': project_name.id,
                                'repetition': hour_to,
                                'total_hours': repetition_nb,
                                }
                            course_name = course_obj.create(course_vals)
                            logger.info("___________course_vals________: %s ",course_name) 
                    
                    if place_id:
                        logger.info("_place_id__id______________: %s ",place_id)
                        place_name = place_obj.search([('name', '=', place_id)])
                        if not place_name:
                            place_vals ={
                                'name': place_id, 
                                'referent': 0,
                                
                                }
                            place_name = place_obj.create(place_vals)
                            logger.info("___________place_vals________: %s ",place_name)   
                                      
                    if date_lesson:
                        lesson_id = lesson_obj.search([('date', '=', date_lesson),
                                                       ('start_time','!=',start_obj),
                                                       ('end_time','!=',end_obj)])
#                                                       , ('teacher_id','!=',record.id)
                        logger.info("_lesson_id______________: %s ",lesson_id)

                        if lesson_id:
                            raise UserError(_('This date already exists for the lesson!'))

                        if not lesson_id:
                            lesson_vals={
                                'date': date_lesson,
                                'start_time': start_obj,
                                'end_time': end_obj,
                                'teacher_id': teacher_name.id,
#                                 'project_id': project_name.id,
                                'course_id': course_name.id,
                                'place': place_name.id,
                                }    
                            logger.info("_lesson_vals______________: %s ",lesson_vals)
                            lesson_id = lesson_obj.create(lesson_vals) 

            self.write({'state':'done'})         
        return True             
                   
                        
 
    