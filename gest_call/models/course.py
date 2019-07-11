from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
from mako.runtime import _inherit_from
logger=logging.getLogger('_______LOGGER B____________')

class hr_employee(models.Model):
   _inherit = 'hr.employee'
   
   gest_course_id = fields.Many2one('gestcal.course',string='Gest cal id')

class GestcalCourse(models.Model):
   
    _name = 'gestcal.course'
    _rec_name = 'name'
    _description = 'Gestcal Course'
    
    name = fields.Char(string='Name')
    repetition = fields.Integer(string='Repetition')
    total_hours = fields.Float(string='Total Hours')
    topics = fields.Many2one('gestcal.course.topics',string='Topics')
    lesson_id = fields.One2many('gestcal.lesson','course_id', string='Lesson') 
    attachments_ids = fields.One2many('gestcal.attachment', 'courses_id', string='Attachment')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    courses_ids =  fields.Many2one('gestcal.project', string='Courses') 
    project_id = fields.Many2one('gestcal.project', string='Project')
    
    teacher_ids = fields.One2many('hr.employee', 'gest_course_id', string='Teacher')
    recipients_ids = fields.One2many('res.partner', 'gest_course_id', string='Recipients')

    def get_teachers (self):
        teacher_list = [] 
        value = {}
        for rec in self.lesson_id:
            if rec.teacher_id.id not in teacher_list:
                teacher_list.append(rec.teacher_id.id)

        print('teacher_list',teacher_list) 
        self.write({'teacher_ids' : [(6,0,teacher_list)]})
        return  
    
    
    def get_recipients (self):
        teacher_list = [] 
        value = {}
        for rec in self.lesson_id:
            if rec.teacher_id.id not in teacher_list:
                teacher_list.append(rec.teacher_id.id)

        print('teacher_list',teacher_list) 
        self.write({'teacher_ids' : [(6,0,teacher_list)]})
        return  
    
    
    def _compute_attachment_count(self):
        for attachment in self:
            attachment.attachment_count = len(attachment.attachments_ids)

    @api.multi
    def attachment_action_to_open(self):
        ''' This opens the xml view specified in xml_id for the current attachment '''
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')

        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('gest_call', xml_id)
            res.update(
                context={'default_courses_id': self.id,
                         },
                domain=[('courses_id', '=', self.id)]
            )
            return res
        
        return False

    
class GestcalCourse_topics(models.Model):
   
    _name = 'gestcal.course.topics'
    
    name = fields.Char(string='Name')
    text = fields.Text(string='Text') 
    
    