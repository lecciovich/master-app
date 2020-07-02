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

    participation_hour = fields.Float(string='Participation hours', compute='get_participation_hours', digits=(2, 2),
                                      help='Time according to timeformat of 24 hours')#, store=True
    tot_inserted_hours = fields.Float(string='Total Inserted Hours', compute='get_inserted_hours', digits=(2, 2),
                                      help='Time according to timeformat of 24 hours')
    # participation_hour = fields.Float(compute='', string='Participation Hour')


    state = fields.Selection([
        ('active', 'Active'),
        ('withdrawed', 'Withdrawed')
    ], oldname='recipient_state', string='Status', readonly=True, default='active', index=True, copy=False)  #, track_visibility='onchange'copy=False, index=True,    # , store=True, copy=False
        # default='active', track_visibility='onchange' store=True, readonly=True, recipient_, default='active', readonly=True
    # , readonly = True, index = True, copy = False, track_visibility = 'onchange'
    # ], string='Recipient_Status', index=True, readonly=True, default='active')
    # , string = 'Recipient_Status', readonly = True, default = 'active'
    #, readonly=True, default='active',
        # track_visibility='onchange'
    @api.one
    @api.depends('gest_course_id')
    def get_participation_hours(self):
        tot_participation_hours = 0
        for course in self.gest_course_id:
            for lesson in course.lesson_ids:
                if lesson.check_done():
                    tot_participation_hours = self.sum_duration(
                        tot_participation_hours, self.sub_duration(lesson.end_time, lesson.start_time))

        print(dict(self._fields['state'].selection).get(self.state))
        # provo con self.search
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
                tot_hours = self.sum_duration(tot_hours,
                                              self.sub_duration(lesson.end_time, lesson.start_time))
        self.tot_inserted_hours = tot_hours

    @api.one
    def course_withdraw(self):
        return self.write({'state': 'withdrawed'})

    @api.one
    def course_rejoin(self):
        return self.write({'state': 'active'})

    def sum_duration(self, duration1, duration2):
        [min_of_hour1, min_of_hour2] = [duration1 // 1 * 60, duration2 // 1 * 60]
        sum_minutes = (min_of_hour1 + (duration1-duration1 // 1) * 100) + (min_of_hour2 + (duration2-duration2 // 1) * 100)
        float_hour = sum_minutes // 60
        float_min = (sum_minutes - 60 * float_hour) / 100
        sum_time = float_hour + float_min
        return sum_time

    def sub_duration(self, duration1, duration2):
        [min_of_hour1, min_of_hour2] = [duration1 // 1 * 60, duration2 // 1 * 60]
        sub_minutes = (min_of_hour1 + (duration1-duration1 // 1) * 100) - (min_of_hour2 + (duration2-duration2 // 1) * 100)
        float_hour = sub_minutes // 60
        float_min = (sub_minutes - 60 * float_hour) / 100
        sum_time = float_hour + float_min
        return sum_time
