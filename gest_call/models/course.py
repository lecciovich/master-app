from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')


class GestcalCourse(models.Model):
   
    _name = 'gestcal.course'
    _rec_name = 'name'
    _description = ' Gestcal Course'
    
    name = fields.Char(string='Name')
    repetition = fields.Integer(string='Repetition') # I'm not sure about this field: Repetition should represent the 1st, 2nd, 3rd, etc, repetition of 
                                                     # the same course (so, hours, teacher, title are identical) BUT with DIFFERENT STUDENTS. It's basically ID for the user.
    total_hours = fields.Float(string='Total Hours')
    topics = fields.Char(string='Topics')
    lesson_id = fields.One2many('gestcal.lesson','course_id', string='Lesson') # same of line 48: shouldn't this be One2many? Each course have many lessions date
    attachments_ids = fields.One2many('gestcal.attachment', 'courses_id', string='Attachment')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    courses_ids =  fields.Many2one('gestcal.project', string='courses') 


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
