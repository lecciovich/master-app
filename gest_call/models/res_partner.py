# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
 
    lesson_id = fields.Many2one('gestcal.lesson', 'lesson')
    projects_ids = fields.Many2one('gestcal.project', 'project')
    is_student = fields.Boolean(string='Is a Student?')
    is_teacher = fields.Boolean(string='Is a Teacher?')
    is_operator = fields.Boolean(string='Is a Operator?')
    
    gest_course_id = fields.Many2one('gestcal.course',string='gest cal id')
    recipients_course_id = fields.Many2one('gestcal.course',string='gest cal id')
    plan_ids = fields.Many2many('gestcal.plan','partner_plan_rel', 'partner_id', 'plan_id', string='Plan',store=True)

    topics = fields.Many2many('gestcal.course.topics',string='Topics')

    participation_hour = fields.Float(string='Participation hours', compute='get_participation_hours')
    tot_inserted_hours= fields.Float(string='Total Inserted Hours', compute='get_inserted_hours')


    @api.one
    @api.depends('recipients_course_id')
    def get_participation_hours(self):
        tot_participation_hours=0
        for course in self.recipients_course_id:
            for lesson in course.lesson_ids:
                if lesson.check_done():
                    tot_participation_hours+=(lesson.end_time-lesson.start_time)
        self.participation_hour=tot_participation_hours

    @api.one
    @api.depends('recipients_course_id')
    def get_inserted_hours(self):
        tot_hours=0
        for course in self.recipients_course_id:
            for lesson in course.lesson_ids:
                tot_hours+=(lesson.end_time-lesson.start_time)
        self.tot_inserted_hours=tot_hours
