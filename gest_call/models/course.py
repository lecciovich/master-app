from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')


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
    
    teacher_ids = fields.One2many('gestcal.course.teacher', 'course_id', string='Teacher')

    def get_teachers (self):
        lesson = self.env['gestcal.lesson'].search([])
         
        teacher_list = [] 
        value = {}
        for rec in lesson:
            if rec.course_id.id == self.id:
                print(rec.teacher_id.name)
 
                teacher_list.append([0,0,{
                                    'teacher_name':  rec.teacher_id.id,  
                                    'lesson_id': rec.id,
                                }])
        print('teacher_list',teacher_list)
#         self.teacher_ids = teacher_list
        self.write({'teacher_ids' : teacher_list})
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

class GestcalCourse_teacher(models.Model):
   
    _name = 'gestcal.course.teacher'
    
    teacher_name = fields.Many2one('hr.employee', string='Teacher')
    lesson_id = fields.Many2one('gestcal.lesson', string='Lesson') 
    course_id = fields.Many2one('gestcal.course', string='Courses') 
    
class GestcalCourse_topics(models.Model):
   
    _name = 'gestcal.course.topics'
    
    name = fields.Char(string='Name')
    text = fields.Text(string='Text') 