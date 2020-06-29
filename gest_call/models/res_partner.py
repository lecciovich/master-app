# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import logging
logger = logging.getLogger('_______LOGGER B____________')


class ResPartner(models.Model):
    _inherit = 'res.partner'
 
    lesson_id = fields.Many2one('gestcal.lesson', 'lesson')
    projects_ids = fields.Many2one('gestcal.project', 'project')
    is_student = fields.Boolean(string='Is a Student?')
    is_teacher = fields.Boolean(string='Is a Teacher?')
    is_operator = fields.Boolean(string='Is a Operator?')
    
    gest_course_id = fields.Many2many('gestcal.course', string='gest cal id') #, compute='get_courses', 'recipients_id', , compute='get_courses'
    #gest_course_id = fields.Many2one('gestcal.course', string='gest cal id') #'recipients_ids',
    plan_ids = fields.Many2many('gestcal.plan', 'partner_plan_rel', 'partner_id', 'plan_id', string='Plan', store=True)
    topics = fields.Many2many('gestcal.course.topics', string='Topics')
    participation_hour = fields.Float(string='Participation hours', compute='get_participation_hours', digits=(2, 2),
                                      help='Time according to timeformat of 24 hours', store=True)
    tot_inserted_hours = fields.Float(string='Total Inserted Hours', compute='get_inserted_hours', digits=(2, 2),
                                      help='Time according to timeformat of 24 hours')
    # participation_hour = fields.Float(compute='', string='Participation Hour')


    state = fields.Selection([
        ('active', 'Active'),
        ('withdrawed', 'Withdrawed')
    ], oldname='recipient_state', string='Recipient_Status', index=True, copy=False, readonly=True, default='active', track_visibility='onchange') #, track_visibility='onchange'copy=False, index=True,

    # @api.one
    # def get_courses(self):
    #     for record in self:
    #         course_list = []
    #         # for rec in gestcal.course:
    #         #     if rec. not in teacher_list:
    #         #         teacher_list.append(rec.teacher_id.id)
    #         #     logger.info('__________teacher_list________: %s  ', teacher_list)
    #         course_list = self.env['gestcal.course'].search([[record, 'in', 'recipients_ids'], ['customer', '=', True]])
    #         record.write({'gest_course_id': [(6, 0, course_list)]})
    #     return

    # domain = [(, 'is in', 'recipients_ids')]
    # @api.depends('')
    # def get_courses(self):
    #     for rec in self:
    #         if rec.is_student:
    #             for course in self.env['gestcal.course'].search([(rec, 'in', 'recipients_ids')]):
    #                 self.write({'gest_course_id': course})


    @api.one
    @api.depends('gest_course_id')
    def get_participation_hours(self):#, cr, uid, ids, context=None
        tot_participation_hours = 0
        logger.info('__________courseid_context________: %s  ', self.env.context.get('course_id'))
        course_id_sel = self.env.context.get('course_id')
        logger.info('__________course_id_sel________: %s  ', course_id_sel)
        for course in self.gest_course_id:
            if course_id_sel == course.course_id:
                for lesson in course.lesson_ids:
                    if lesson.check_done():
                        tot_participation_hours = self.sum_duration(
                            tot_participation_hours, self.sub_duration(lesson.end_time, lesson.start_time))
        print(dict(self._fields['state'].selection).get(self.state))
        #provo con self.search
        if self.state == 'active':
            self.participation_hour = tot_participation_hours
        else:
            pass

    # @api.one
    # @api.depends('gest_course_id')
    # def get_inserted_hours(self):
    #     tot_hours = 0
    #
    #     self.gest_course_id.write(context['course_id'])
    #     # for course in self.gest_course_id:
    #     #     if context['course_id'] == course.course_id:
    #     for lesson in self.gest_course_id.lesson_ids:
    #         tot_hours = self.sum_duration(tot_hours,
    #                                       self.sub_duration(lesson.end_time, lesson.start_time))
    #     self.tot_inserted_hours = tot_hours
    @api.one
    @api.depends('gest_course_id')
    def get_inserted_hours(self):
        tot_hours = 0
        logger.info('__________courseid_context________: %s  ', self.env.context.get('course_id'))
        course_id_sel = self.env.context.get('course_id')
        logger.info('__________course_id_sel________: %s  ', course_id_sel)
        for course in self.gest_course_id:
            if course_id_sel == course.course_id:
                for lesson in course.lesson_ids:
                    tot_hours = self.sum_duration(tot_hours,
                                                  self.sub_duration(lesson.end_time, lesson.start_time))
        self.tot_inserted_hours = tot_hours

    @api.one
    def course_withdraw(self):
        # self.get_participation_hours()
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


