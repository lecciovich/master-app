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
    #gest_course_id = fields.Many2one('gestcal.course', string='gest cal id') #'recipients_ids',
    plan_ids = fields.Many2many('gestcal.plan', 'partner_plan_rel', 'partner_id', 'plan_id', string='Plan', store=True)

    topics = fields.Many2many('gestcal.course.topics', string='Topics')

    participation_hour = fields.Float(string='Participation hours', compute='get_participation_hours')
    tot_inserted_hours = fields.Float(string='Total Inserted Hours', compute='get_inserted_hours')
    state = fields.Selection([
        ('active', 'Active'),
        ('withdrawed', 'Withdrawed')
    ], oldname='recipient_state', string='Recipient_Status', index=True, copy=False, readonly=True, default='active', track_visibility='onchange') #, track_visibility='onchange'copy=False, index=True,



    @api.one
    @api.depends('gest_course_id')
    def get_participation_hours(self):
        tot_participation_hours = 0
        for course in self.gest_course_id:
            for lesson in course.lesson_ids:
                if lesson.check_done():
                    tot_participation_hours += (lesson.end_time - lesson.start_time)
        print(dict(self._fields['state'].selection).get(self.state))

        if self.state == 'active':
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

    @api.one
    def course_withdraw(self):
        return self.write({'state': 'withdrawed'})

    @api.one
    def course_rejoin(self):
        return self.write({'state': 'active'})
