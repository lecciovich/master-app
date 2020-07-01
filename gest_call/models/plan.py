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
    plan_code = fields.Char(string='Plan code', required=True)
    # found = fields.Float('Found', required=True)
    financing_amount = fields.Float('Financing Amount', required=True)
    total_lesson_hours = fields.Integer('Total Lesson Hours')
    call = fields.Many2one('gestcal.call', string='Call title')
    submission = fields.Date(string='Submission')
    admittance = fields.Date(string='Admittance')
    agreement = fields.Date(string='Agreement')
    deadline = fields.Datetime(string='Deadline')
    lessons_start = fields.Date(string='Lesson start')
    report_submission = fields.Date(string='Report Submission')
    # account_request = fields.Date(string='Account Request')
    partner = fields.Many2many('res.partner', 'partner_plan_rel', 'plan_id', 'partner_id', string='Partner',store=True)
    operative_partner = fields.Many2many('res.partner','partner_plan_rel', 'plan_id', 'partner_id', string='Operative Partner',store=True)
    projects = fields.Many2many('gestcal.project','project_ids', string='Projects')
    attachments_ids = fields.One2many('gestcal.attachment', 'projects_id', string='Attachment')
    attachments = fields.Many2one('gestcal.attachment', string='Attachments')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    plan_host = fields.Many2one('res.partner', string='Plan host', domain=[('is_company', '=', True)])
    plan_actuator = fields.Many2one('res.partner', string='Plan actuator', domain=[('is_company', '=', True)])
    plan_handler = fields.Many2one('res.partner', string='Plan handler', domain=[('is_operator', '=', True)])
    total_recipients = fields.Integer('Total recipients')
    plan_director = fields.Many2one('res.partner', string='Plan Director', domain=[('is_company', '=', False)])
    beneficiary_representative = fields.Many2one('res.partner', string='Beneficiary Representative', domain=[('is_company', '=', False)])
    plan_assistant = fields.Many2one('res.partner', string= 'Plan assistent', domain=[('is_company', '=', False),('is_operator', '=', True)])
    auditor = fields.Many2one('res.partner', string='Unique Auditor', domain=[('is_company', '=', False)])

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('active', 'Active'), 
        ('completed','Completed'), 
        ('accounted','Sent To Financial Director'), 
        ('closed','Closed')
        
        ], string='Status', index=True, readonly=True, copy=False, default='draft', track_visibility='onchange')


    def count_lesson_hours(self):
        for record in self:
            for project in record.projects:
                self.env('gestcal.course').search([('project_id', '=', project.project_id)])

    def _compute_attachment_count(self):
        for attachment in self: 
            attachment.attachment_count = len(attachment.attachments_ids)
            logger.info('___________count________: %s  ',attachment.attachment_count)

    @api.one
    @api.constrains('plan_code')
    def _check_plan_code(self):
        title = self.title
        for record in self:
            code_plan = self.search([('plan_code','=',record.plan_code),('id','!=',record.id)])
            lenplan = len(code_plan) + 1
            if code_plan:
                self.title = str(title) + '(' + (str(lenplan))+')'
 
    @api.multi
    def draft_plan(self):
        return self.write({'state': 'draft'})
                
    @api.multi
    def submitted_plan(self):
        return self.write({'state': 'submitted'})

    @api.multi
    def active_plan(self):
        return self.write({'state': 'active'})

    @api.multi
    def completed_plan(self):
        # Questo stage scatta se e solo se la somma delle ore dei corsi coincide con la  dkj
        # ciclo sui record di lesson e sui lesson_id di self e se coincidono addo oggetto a lista
        tot_lesson_hours = 0
        done_lesson_hours = 0

        for project in self.projects:
            for course in project.courses:
                tot_lesson_hours += course.total_hours
                for lesson in course.lesson_ids:
                    if lesson.check_done():
                        done_lesson_hours += (lesson.end_time-lesson.start_time)
                        logger.info('__________done_lesson_hours_list________: %s  ', done_lesson_hours)
        if done_lesson_hours >= self.total_lesson_hours:
            return self.write({'state': 'completed'})
        else:
            print('error: lesson hours completed doesn\'t match with plan agreement')

        #             if lesson.search(['date','<', current_date],['end_time','<',current_hour]):
        #                 done_lesson_hours+=(lesson.end_time-lesson.start_time)
        #             # if str(lesson.date)<current_date and lesson.end_time<float(datetime.now().strftime("%H.%M")):
        #             #     done_lesson_hours+=(lesson.end_time-lesson.start_time)
        # if tot_lesson_hours==done_lesson_hours:
        #     return self.write({'state': 'completed'})

    @api.multi
    def accounted_plan(self):
        return self.write({'state': 'accounted'})

    @api.multi
    def closed_plan(self):
        return self.write({'state': 'closed'})


class Call(models.Model):
    _name = 'gestcal.call'
    _rec_name = 'title'
    _description = 'Gestcal Call'

    title = fields.Char(string='Call title')

