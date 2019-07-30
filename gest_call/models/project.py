from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')


class GestcalProject(models.Model):
 
    _name = 'gestcal.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'
    _description = 'Gestcal project'
    
    title = fields.Char(string='Title', required=True)
    project_code = fields.Char(string='Project code' ,required=True)
    # found = fields.Float('Found', required=True)
    financing_amount = fields.Float('Financing Amount', required=True)
    total_lesson_hours = fields.Float('Total Lesson Hours')
    call = fields.Char(string='Call')
    submission = fields.Date(string='Submission')
    admittance = fields.Date(string='Admittance')
    agreement = fields.Date(string='Agreement')
    account_request = fields.Date(string='Account Request')
    partner = fields.Many2many('res.partner','projects_ids', string='Partner')
    deadline = fields.Datetime(string='Deadline')
    courses = fields.Many2many('gestcal.course','courses_ids', string='Courses')
    attachments_ids = fields.One2many('gestcal.attachment', 'projects_id', string='Attachment')
    attachments = fields.Many2one('gestcal.attachment', string='Attachments')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('active', 'Active'), 
        ('completed','Completed'), 
        ('accounted','Sent To Financial Director'), 
        ('closed','Closed')
        
        ], string='Status', index=True, readonly=True, copy=False, default='draft', track_visibility='onchange')


    def _compute_attachment_count(self):
        for attachment in self: 
            attachment.attachment_count = len(attachment.attachments_ids)
            logger.info('___________count________: %s  ',attachment.attachment_count)
            
    @api.constrains('project_code','title')
    def _check_name(self):
        if self.title ==  self.project_code:
            raise ValidationError(_('Two project Title and Project code can not be the same'))
 
    @api.multi
    def attachment_action_to_open(self):
        ''' This opens the xml view specified in xml_id for the current attachment '''
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')

        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('gest_call', xml_id)
            res.update(
                context={'default_projects_id': self.id,
                         },
                domain=[('projects_id', '=', self.id)]
            )
            logger.info('___________res________: %s  ',res)
            return res
            
        return False

    @api.multi
    def submitted_project(self):
        return self.write({'state': 'submitted'})

    @api.multi
    def active_project(self):
        return self.write({'state': 'active'})

    @api.multi
    def completed_project(self):
        return self.write({'state': 'completed'})

    @api.multi
    def accounted_project(self):
        return self.write({'state': 'accounted'})

    @api.multi
    def closed_project(self):
        return self.write({'state': 'closed'})



