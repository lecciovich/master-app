from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')


class GestcalAttachment(models.Model):
   
    _name = 'gestcal.attachment'
    _rec_name = 'name'
    
    name = fields.Char(string='Name')
    description = fields.Char(string='Name')
    validity = fields.Datetime(string='Validity')
    type = fields.Char(string='Type')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachment')
    projects_id = fields.Many2one('gestcal.project', string='projects_id') 
#     contacts_id = fields.Many2one('res.partner', string='contacts_id')
    courses_id = fields.Many2one('gestcal.course', string='courses_id')
#     classrooms_id = fields.Many2one('gestcal.classrooms', string='classrooms_id')

    
