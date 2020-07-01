# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    lesson_id = fields.Many2one('gestcal.lesson', 'lesson')
    projects_ids = fields.Many2one('gestcal.project', 'project')
    is_student = fields.Boolean(string='Is a Student?')
    is_teacher = fields.Boolean(string='Is a Teacher?')
    is_operator = fields.Boolean(string='Is a Operator?')
    
    gest_course_id = fields.Many2one('gestcal.course', string='gest cal id')
    # recipients_course_id = fields.Many2one('gestcal.course', string='gest cal id')
    plan_ids = fields.Many2many('gestcal.plan', 'partner_plan_rel', 'partner_id', 'plan_id', string='Plan', store=True)

    topics = fields.Many2many('gestcal.course.topics', 'course_topic_rel', 'res_partner_id', 'topic_id', string='Topics')

    participation_hour = fields.Float(string='Participation hours', compute='get_participation_hours')
    tot_inserted_hours = fields.Float(string='Total Inserted Hours', compute='get_inserted_hours')

    recipient_state = fields.Selection([
        ('active', 'Active'),
        ('withdrawed', 'Withdrawed')
    ], string='Recipient_Status', default='active', readonly=True, index=True, copy=False, track_visibility='onchange')# , store=True, copy=False
        # default='active', track_visibility='onchange' store=True, readonly=True, recipient_, default='active', readonly=True
    # , readonly = True, index = True, copy = False, track_visibility = 'onchange'


    @api.one
    @api.depends('gest_course_id')
    def get_participation_hours(self):
        tot_participation_hours = 0
        for course in self.gest_course_id:
            for lesson in course.lesson_ids:
                if lesson.check_done():
                    tot_participation_hours += (lesson.end_time - lesson.start_time)
        print(dict(self._fields['recipient_state'].selection).get(self.recipient_state))
        # dict(self._fields['recipient_state'].selection).get(self.recipient_state)
        if self.recipient_state == 'active':
            self.participation_hour = tot_participation_hours
        else:
            pass

    @api.one
    @api.depends('gest_course_id')
    def get_inserted_hours(self):
        tot_hours = 0
        for course in self.gest_course_id:
            for lesson in course.lesson_ids:
                tot_hours += (lesson.end_time-lesson.start_time)
        self.tot_inserted_hours = tot_hours

    @api.multi
    @api.constrains('gest_course_id')
    def course_withdraw(self):
        return self.write({'state': 'withdrawed'})
