from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')


class GestcalPlan(models.Model):
 
    _name = 'gestcal.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'
    _description = 'Gestcal Plan'
    
    title = fields.Char(string='Title', required=True)
    plan_code = fields.Char(string='Plan code' ,required=True)
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
    projects = fields.Many2many('gestcal.project','project_ids', string='Projects')
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
            
    @api.constrains('plan_code','title')
    def _check_name(self):
        if self.title ==  self.plan_code:
            raise ValidationError(_('Two project Title and Project code can not be the same'))
 
    @api.multi
    def submitted_plan(self):
        return self.write({'state': 'submitted'})

    @api.multi
    def active_plan(self):
        return self.write({'state': 'active'})

    @api.multi
    def completed_plan(self):
        return self.write({'state': 'completed'})

    @api.multi
    def accounted_plan(self):
        return self.write({'state': 'accounted'})

    @api.multi
    def closed_plan(self):
        return self.write({'state': 'closed'})



