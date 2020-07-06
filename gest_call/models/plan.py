import pytz

from odoo import models, fields, api, _
from datetime import datetime, date
import time
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger('_______LOGGER B____________')


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
    # plan steps date: draft always
    submission = fields.Date(string='Submission')#, default=lambda * a: time.strftime('%Y-%m-%d')
    agreement = fields.Date(string='Agreement')
    admittance = fields.Date(string='Admittance')
    lessons_start = fields.Date(string='Lesson start')
    deadline = fields.Date(string='Deadline')  #Datetime
    report_submission = fields.Date(string='Report Submission')#, default=lambda * a: time.strftime('%Y-%m-%d')

    # account_request = fields.Date(string='Account Request')
    partner = fields.Many2many('res.partner', 'partner_plan_rel', 'plan_id', 'partner_id', string='Partner', store=True)
    operative_partner = fields.Many2many('res.partner', string='Operative Partner',
                                         domain=[('is_company', '=', True)], store=True)
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
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('accounted', 'Sent To Financial Director')

        ], string='Status', index=True, readonly=True, copy=False, default='draft', track_visibility='onchange')


    def count_lesson_hours(self):
        for record in self:
            for project in record.projects:
                self.env('gestcal.course').search([('project_id', '=', project.project_id)])

    def _compute_attachment_count(self):
        for attachment in self: 
            attachment.attachment_count = len(attachment.attachments_ids)
            logger.info('___________count________: %s  ', attachment.attachment_count)

    @api.one
    @api.constrains('plan_code')
    def _check_plan_code(self):
        title = self.title
        for record in self:
            code_plan = self.search([('plan_code','=',record.plan_code),('id','!=',record.id)])
            lenplan = len(code_plan) + 1
            if code_plan:
                self.title = str(title) + '(' + (str(lenplan))+')'
 
    @api.one
    def draft_plan(self):
        return self.write({'state': 'draft'})
                
    # @api.one
    @api.multi
    def submitted_plan(self):
        system_tz = self.env.context.get('tz') or self.env.user.tz
        if not system_tz:
            system_tz = "UTC"
        user_tz = pytz.timezone(system_tz)
        current_date = str(datetime.now().astimezone(user_tz).date().strftime('%Y-%m-%d'))

        if self.submission:
            plan_submission = self.env['gestcal.plan'].search([('submission', '<=', current_date)])
            if self in plan_submission:
                return self.write({'state': 'submitted'})
            elif self.state != 'draft':
                # raise ValueError(_('Submission date assigned is not present or past date'))
                self.draft_plan()

    @api.multi
    def revert_to_submitted_plan(self):
        return self.submitted_plan()

    @api.multi
    def active_plan(self):
        system_tz = self.env.context.get('tz') or self.env.user.tz
        if not system_tz:
            system_tz = "UTC"
        user_tz = pytz.timezone(system_tz)
        current_date = str(datetime.now().astimezone(user_tz).date().strftime('%Y-%m-%d'))

        if self.agreement:
            plan_agreement = self.env['gestcal.plan'].search([('agreement', '<=', current_date)])
            if self in plan_agreement:
                return self.write({'state': 'active'})
            elif self.state != 'submitted':
                self.submitted_plan()

    @api.multi
    def completed_plan(self):
        system_tz = self.env.context.get('tz') or self.env.user.tz
        if not system_tz:
            system_tz = "UTC"
        user_tz = pytz.timezone(system_tz)
        current_date = str(datetime.now().astimezone(user_tz).date().strftime('%Y-%m-%d'))

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
        if done_lesson_hours >= self.total_lesson_hours * (70 / 100):  # and self.admittance <= current_date
            if self.admittance:
                plan_admittance = self.env['gestcal.plan'].search([('admittance', '<=', current_date)])
                if self in plan_admittance:
                    return self.write({'state': 'completed'})
            # return self.write({'state': 'completed'})
        else:
            print('error: lesson hours completed doesn\'t match with plan agreement or admittance date is not reached yet')
            if self.state != 'active':
                return self.active_plan()
            # raise ValidationError (_('error: lesson hours completed doesn\'t match with plan agreement'))

        #             if lesson.search(['date','<', current_date],['end_time','<',current_hour]):
        #                 done_lesson_hours+=(lesson.end_time-lesson.start_time)
        #             # if str(lesson.date)<current_date and lesson.end_time<float(datetime.now().strftime("%H.%M")):
        #             #     done_lesson_hours+=(lesson.end_time-lesson.start_time)
        # if tot_lesson_hours==done_lesson_hours:
        #     return self.write({'state': 'completed'})

    @api.multi
    def closed_plan(self):
        system_tz = self.env.context.get('tz') or self.env.user.tz
        if not system_tz:
            system_tz = "UTC"
        user_tz = pytz.timezone(system_tz)
        current_date = str(datetime.now().astimezone(user_tz).date().strftime('%Y-%m-%d'))

        if self.agreement:
            plan_deadline = self.env['gestcal.plan'].search([('deadline', '<=', current_date)])
            if self in plan_deadline:
                return self.write({'state': 'closed'})
            elif self.state != 'completed':
                return self.completed_plan()

    @api.multi
    def accounted_plan(self):
        system_tz = self.env.context.get('tz') or self.env.user.tz
        if not system_tz:
            system_tz = "UTC"
        user_tz = pytz.timezone(system_tz)
        current_date = str(datetime.now().astimezone(user_tz).date().strftime('%Y-%m-%d'))

        if self.agreement:
            plan_report_submission = self.env['gestcal.plan'].search([('report_submission', '<=', current_date)])
            if self in plan_report_submission:
                return self.write({'state': 'accounted'})
            elif self.state != 'closed':
                return self.closed_plan()

    # @api.multi
    # def closed_plan(self):
    #     return self.write({'state': 'closed'})


class Call(models.Model):
    _name = 'gestcal.call'
    _rec_name = 'title'
    _description = 'Gestcal Call'

    title = fields.Char(string='Call title')

