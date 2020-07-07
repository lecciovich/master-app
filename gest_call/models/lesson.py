from odoo import models, fields, api, _
from datetime import datetime, timedelta
import time
import pytz
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger('_______LOGGER B____________')

class GestcalLesson(models.Model):

    _name = 'gestcal.lesson'
    _rec_name = 'date'
    _description = 'Gestcal lesson'
#     _inherit = 'calendar.event'

    date = fields.Date(string='Date', required=True)
    date_start_marco = fields.Datetime(string='Start datetime', compute='datetime_start_calc')
    date_end_marco = fields.Datetime(string='End datetime', compute='datetime_end_calc')
    # .to_string(date.strftime('%Y-%M-%D') + self.start_time)
    # start_time = fields.Datetime(string='Start Time')
    # end_time = fields.Datetime(string='End Time')
    start_time = fields.Float(string='Start Time', required=True, digits=(2, 2),
                              help='Time according to timeformat of 24 hours')
    end_time = fields.Float(string='End Time', required=True, digits=(2, 2),
                            help='Time according to timeformat of 24 hours')
    teacher_id = fields.Many2one('res.partner', string='Teacher', required=True, domain=[('is_teacher', '=', True)]) # each lession have only ONE teacher
    # recipients_id = fields.Many2many('res.partner', 'lesson_id', string='Recipients', domain=[('is_student', '=', True)])#
    recipients_id = fields.Many2many('res.partner', string='Recipients', domain=[('is_student', '=', True)],
                                     copy=True, readonly=False)#, store=True##, store=True ##related='course_id.recipients_ids',
    # 'gestcal.lesson', 'recipients_ids'
    course_id = fields.Many2one('gestcal.course', string='course')
    past_course = fields.Many2one('gestcal.course', string='Past Course')
    project_id = fields.Many2one('gestcal.project', string='Project',  related='course_id.project_id')
    place = fields.Many2one('gestcal.place', string='Place', required=True)
    registry = fields.Many2many('gestcal.lesson.registry',
                                string='Students Presence')  #, store=True , readonly=False, store=True
    @api.onchange('course_id')
    def onchange_course_id(self):
        # old_value = self.past_course
        self.past_course = self.course_id

    @api.multi
    def set_lesson_participations(self):
        for rec in self:
            for recipient in rec.recipients_id:
                recipient.with_context(course_id=rec.course_id.course_id).get_participation_hours()
        return

    @api.multi
    def set_lesson_participations(self):
        for rec in self:
            for recipient in rec.recipients_id:
                recipient.with_context(course_id=rec.course_id.course_id).get_participation_hours()
        return
    # context = "{'course_id':course_id,'lessons':lesson_ids}"

    @api.one
    def get_recipients(self):
        self.write({'recipients_id': [(6, 0, [])]})
        self.write({'registry': [(6, 0, [])]})

        # recipients_list = []#self.recipients_id.id#self.recipients_id.read(self.recipients_id)
        recipients_list = []#self.recipients_id.id#self.recipients_id.read(self.recipients_id)
        current_course_recip = []
        # for course in self.course_id:
        for recipient in self.recipients_id:
            recipients_list.append(recipient.id)
            # self.set_registry(recipient)
        for recipient in self.course_id.recipients_ids:
            recipients_list.append(recipient.id)
            current_course_recip.append(recipient.id)
            self.set_registry(recipient)
        # for recipient in self.recipients_id:
        for recipient_past in self.past_course:
            if recipient_past.id in current_course_recip:
                continue
            else:
                recipients_list.remove(recipient_past.id)
        # # for course in self.course_id:
        # for recipient in self.recipients_id:
        #     recipients_list.append(recipient.id)
        #     self.set_registry(recipient)
        # course = self.course_id
        # for recipient in self.course_id.recipients_ids:
        #     if recipient.id not in recipients_list:
        #         recipients_list.append(recipient.id)
        #         self.set_registry(recipient)
        for recipient in self.recipients_id:
            self.set_registry(recipient)
        logger.info('__________recipients_list________: %s  ', recipients_list)
        self.write({'recipients_id': [(6, 0, recipients_list)]})
        return

    @api.one
    def set_registry(self, recipient):
        # self.write({'registry': [(6, 0, recipients_list)]})
        registry_list = []
        logger.info('___________reg_student________: %s  ', recipient)
        for reg_student in self.registry:
            logger.info('___________reg_student________: %s  ', reg_student)
            if reg_student.student.name == recipient.name:
                #qui posso metterci l'update
                return
            registry_list.append(reg_student.id)
            logger.info('___________registry_list________: %s  ', registry_list)

        vals = {
            'student': recipient.id,
            'lesson': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'time_of_presence': self.sum_duration(self.end_time, -self.start_time)
        }
        reg_recipient = self.env['gestcal.lesson.registry'].create(vals)
        logger.info('___________reg_recipient________: %s  ', reg_recipient)
        registry_list.append(reg_recipient.id)
        logger.info('___________registry_list________: %s  ', registry_list)
        self.write({'registry': [(6, 0, registry_list)]})
        # self.registry = self.env['gestcal.lesson.registry'].create(vals)
        # self.registry.create(vals)
        # self.registry.create({
        #     'student': recipient.id,
        #     'lesson': self.id
        # })
        # self.registry.write({'registry': [(0, 0, recipient)]})
        # self.registry.set_student(recipient)
        # self.registry.set_lesson(self)

    @api.one
    @api.depends('date', 'start_time')
    def datetime_start_calc(self):
        [_, _, _, user_tz] = self.calc_date_and_time_local(datetime.utcnow())

        print(self.date)
        print(self.start_time)
        logger.info('___________start_time________: %s  ', self.start_time)
        logger.info('___________start_date________: %s  ', self.date)

        self.date_start_marco = self.from_t_and_d_to_datetime(self.start_time, self.date, user_tz)

    @api.one
    @api.depends('date', 'end_time')
    def datetime_end_calc(self):
        [_, _, _, user_tz] = self.calc_date_and_time_local(datetime.utcnow())

        print(self.date)
        print(self.end_time)
        logger.info('___________end_time________: %s  ', self.end_time)
        logger.info('___________end_date________: %s  ', self.date)

        self.date_end_marco = self.from_t_and_d_to_datetime(self.end_time, self.date, user_tz)

    def from_t_and_d_to_datetime(self, attr_time, attr_date, tzone):
        strhour = str(attr_time)
        logger.info('___________end_time_string________: %s  ', strhour)
        strdate = str(attr_date)  # .isocalendar()[1]
        logger.info('___________end_date_string________: %s  ', strdate)
        result_datetime = datetime.strptime(str(strdate) + ' ' + str(strhour), '%Y-%m-%d %H.%M')  # .astimezone(user_tz)
        logger.info('___________end_datetime________: %s  ', result_datetime)
        current_datetime = self.convert_TZ_UTC(result_datetime, tzone)
        logger.info('___________datetime_local________: %s  ', current_datetime)  # datetime_local)
        return current_datetime

#     @api.constrains('date','start_time','end_time','teacher_id')
    # def cheking_lesson(self):
#
#         for record in self:
#             logger.info('__________record________: %s  ',record)
#             date = self.search([('date','=',record.date),('id','!=',record.id)])
#             logger.info('___________date________: %s  ',date)
#             
#             date_st = self.search([('start_time','=',record.start_time),('id','!=',record.id)])
#             logger.info('___________date_st________: %s  ',date_st)
#             
#             date_ed = self.search([('end_time','=',record.end_time),('id','!=',record.id)])
#             logger.info('___________date_ed________: %s  ',date_ed)
#             
#             teacher = self.search([('teacher_id','=',record.teacher_id.id),('id','!=',record.id)])
#             logger.info('___________teacher________: %s  ',teacher)
#               
#             if date and date_st and date_ed and teacher: 
#                 raise ValidationError(_('This date already exists for the lesson'))

    @api.one
    @api.constrains('date', 'start_time', 'end_time', 'teacher_id')
    def checking_lesson_teach(self):
        lesson_obj = self.env['gestcal.lesson']

        for rec in lesson_obj.search([]):
            check_teach = rec.search([('date', '=', self.date),
                                      '!', ('start_time', '>=', self.end_time),
                                      '!', ('end_time', '<=', self.start_time),
                                      ('teacher_id.id', '=', self.teacher_id.id)])
            # ('place', '=', self.place),  '&',
            # check_teach = rec.search([('date', '=', self.date),
            #                          ('start_time', '=', self.start_time), ('end_time', '=', self.end_time),
            #                          ('teacher_id.id', '=', self.teacher_id.id)])  # ('place', '=', self.place),
        if len(check_teach) > 1:
            err_str = 'This place ' + self.teacher_id.name + ' already have a lesson at hour selected'
            raise ValidationError(_(err_str))

    @api.one
    @api.constrains('date', 'start_time', 'end_time', 'place')
    def checking_lesson_place(self):
        lesson_obj = self.env['gestcal.lesson']

        for rec in lesson_obj.search([]):
            check_place = rec.search([('date', '=', self.date),
                                      '!', ('start_time', '>=', self.end_time),
                                      '!', ('end_time', '<=', self.start_time),
                                      ('place.id', '=', self.place.id)])  # '&',
        if len(check_place) > 1:
            err_str = 'This place ' + self.place.name + ' already have a lesson at hour selected'
            raise ValidationError(_(err_str))

    @api.one
    @api.constrains('date', 'start_time', 'end_time', 'recipients_id')
    def checking_lesson_recipients(self):
        lesson_obj = self.env['gestcal.lesson'].sudo().search([('id', '!=', self.id)])
        logger.info('___________lesson_obj________: %s  ', lesson_obj)

        recipient_overlapped = []
        check_less = []
        couple_less_recip = []
        for recipient in self.recipients_id:
            for rec in lesson_obj:  # .search([])
                logger.info('___________lesson_obj_rec________: %s  ', rec)
                if recipient in rec.recipients_id:
                    if rec.date == self.date and (not(rec.start_time >= self.end_time or\
                            rec.end_time <= self.start_time)):
                        overlapped_lesson = rec
                        # overlapped_lessons = rec.search([('date', '=', self.date),
                        #                                  ('start_time', '=', self.start_time),
                        #                                  ('end_time', '=', self.end_time)])

                        check_less.append(overlapped_lesson)
                        recipient_overlapped.append(recipient.name)
                        couple_less_recip.append([recipient.name, overlapped_lesson.date, overlapped_lesson.start_time, overlapped_lesson.end_time])
            if len(check_less) >= 1:
                error_msg = 'These recipients: \n'
                # for recipient_lesson in couple_less_recip:
                #     error_msg += recipient_lesson[0] + 'in the lesson in ' + recipient_lesson[1].strptime("%YYYY-%mm-%dd") + 'from' + recipient_lesson[2] + 'to' +'\n'
                for recipient_name in recipient_overlapped:
                    error_msg += recipient_name + '\n'
                error_msg += '\nalready attend a lesson in same time'
                raise ValidationError(_(error_msg))

    @api.one
    @api.constrains('start_time', 'end_time')
    def check_date(self):
        if self.start_time >= self.end_time:
            logger.info('___________check_date________: %s  ', self.start_time > self.end_time)
            raise ValidationError(_('Start time must be greater than end time !'))

    @api.multi
    @api.depends('date', 'start_time', 'end_time')
    def check_done(self):
        [current_date, current_hour, datetime_today, user_tz] = self.calc_date_and_time_local(datetime.utcnow())
        print('datetime today', datetime_today)
        print('date today', current_date)
        print('time today', current_hour)
        print('user tz: ', user_tz)
        logger.info('___________current_date________: %s  ', current_date)
        logger.info('___________current_hour________: %s  ', current_hour)

        logger.info('___________lesson_date________: %s  ', self.date)
        logger.info('___________start_hour________: %s  ', self.start_time)
        logger.info('___________start_hour________: %s  ', self.end_time)

        sameday_date_check = fields.Date().to_string(current_date) == fields.Date().to_string(self.date)
        past_date_check = fields.Date().to_string(current_date) > fields.Date().to_string(self.date)

        past_hour_check = self.trasform_time_in_float(current_hour) > self.end_time #float(current_hour)
        logger.info('___________check_past_date________: %s  ', sameday_date_check)
        logger.info('___________check_float_current_hour________: %s  ', self.trasform_time_in_float(current_hour))
        logger.info('___________check_part_hour________: %s  ', past_hour_check)
        sameday_check = past_date_check or (sameday_date_check and past_hour_check)

        print("date", sameday_date_check, "hour", past_hour_check)
        return sameday_check or current_date > self.date


    def get_now_date_and_time_local(self):
        return self.calc_date_and_time_local(datetime.utcnow())

    def calc_date_and_time_local(self, datetime_arg):
        logger.info('___________current_tz________: %s  ', self.env.context.get('tz'))
        logger.info('___________current_date_hour________: %s  ', self.env.user.tz)
        system_tz = self.env.context.get('tz') or self.env.user.tz
        if not system_tz:
            system_tz = "UTC"
        user_tz = pytz.timezone(system_tz)
        datetime_local = datetime_arg.astimezone(user_tz)
        date_local = datetime_local.date()#.isoformat()
        time_local = datetime.time(datetime_local)#.strftime("%H.%M")
        return date_local, time_local, datetime_local, user_tz

    def set_datetime_given_tz(self, local_time, tzone):
        float_tzone = self.translate_seconds_to_float_time(datetime.utcoffset(tzone).seconds)
        utc_time = local_time - float_tzone
        return utc_time


    def trasform_time_in_float(self, datetime_time):
        logger.info('___________current_date_hour________: %s  ', datetime_time.hour)
        logger.info('___________current_date_hour_from_minute________: %s  ', datetime_time.minute//60)
        logger.info('___________current_date_minute________: %s  ', datetime_time.minute - datetime_time.minute//60)

        tot_seconds = datetime_time.hour * 3600 + datetime_time.minute * 60
        float_time = self.translate_seconds_to_float_time(tot_seconds)
        return float_time

    def sum_duration(self, duration1, duration2):
        # sum_minutes = duration1 * 100 + duration2 * 100
        if duration2 >= 0:
            sum_minutes = self.translate_float_time_to_min(duration1) + self.translate_float_time_to_min(duration2)
        else:
            sum_minutes = self.translate_float_time_to_min(duration1) - self.translate_float_time_to_min(abs(duration2))
        sum_minutes = round(sum_minutes)
        sum_time = self.translate_seconds_to_float_time(sum_minutes * 60)
        return sum_time

    def translate_float_time_to_min(self, float_time):
        min_before_comma = (float_time // 1 * 60)
        min_after_comma = (float_time - float_time // 1) * 100
        return min_before_comma + min_after_comma

    def translate_seconds_to_float_time(self, time_in_seconds):
        time_in_minutes = time_in_seconds // 60
        hours = time_in_minutes // 60
        float_time = hours + (time_in_minutes - hours * 60) / 100
        return float_time

    @api.multi
    def saveandcreate(self):#, cr, uid, ids, context=None
        return {
            'name': 'gestcal.lesson.form',
            'res_model': 'gestcal.lesson',
            'type': 'ir.actions.act_window',
            'context': {},
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('gest_call.view_gestcal_lesson_form').id,
            'target': 'current',
        }

    def convert_TZ_UTC(self, TZ_datetime, tzone):
        fmt = "%YYYY-%mm-%dd %HH:%MM"
        # Current time in UTC
        now_utc = datetime.utcnow()
        # Convert to current user time zone
        now_timezone = now_utc.astimezone(tzone)
        UTC_OFFSET_TIMEDELTA = datetime.strptime(now_utc.strftime(fmt), fmt) - datetime.strptime(
            now_timezone.strftime(fmt), fmt)
        local_datetime = datetime.strptime(TZ_datetime.strftime(fmt), fmt)
        result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
        return result_utc_datetime


class GestcalResPartner_Registry(models.Model):
    _name = 'gestcal.lesson.registry'
    _description = 'Lesson student presence attributes'
    _rec_name = 'student'

    # @api.one
    # @api.depends('end_time', 'start_time')
    # @api.model
    def _get_default_time_of_presence(self):
        return self.sum_duration(self.env.context.get('start_time'), self.env.context.get('end_time'))
        # return self.env.sum_duration(self.end_time, self.end_time)#self.sum_duration(self.end_time, self.end_time)#-

    student = fields.Many2one('res.partner', string='Student', required=True)
    lesson = fields.Many2one('gestcal.lesson', string='Lesson')
    time_of_presence = fields.Float(
        string='Participation time')  ##default=lambda self: self._get_default_time_of_presence()  , compute='_get_default_time_of_presence'
    # withdraw = fields.Char(string='Future withdraw attribute') #lambda a: a._get_default_time_of_presence()##, default=lambda self: self._context.get('start_time')
    start_time = fields.Float(string='Start Time', required=True, digits=(2, 2),
                              help='Time according to timeformat of 24 hours')  # , default=_get_default_time_of_presence()
    # 'gestcal.lesson', 'start_time',  , related='lesson.start_time'   , default=_get_default_time_of_presence
    end_time = fields.Float(string='End Time', required=True, digits=(2, 2),
                            help='Time according to timeformat of 24 hours')

    # 'gestcal.lesson', 'end_time', , related='lesson.end_time'

    # @api.model

    def sum_duration(self, duration1, duration2):
        # sum_minutes = duration1 * 100 + duration2 * 100
        sum_minutes = self.translate_float_time_to_min(duration1) + self.translate_float_time_to_min(duration2)
        sum_time = self.translate_seconds_to_float_time(sum_minutes * 60)
        return sum_time

    def translate_float_time_to_min(self, float_time):
        min_before_comma = (float_time // 1 * 60)
        min_after_comma = (float_time - float_time // 1) * 100
        return min_before_comma + min_after_comma

    def translate_seconds_to_float_time(self, time_in_seconds):
        time_in_minutes = time_in_seconds // 60
        hours = time_in_minutes // 60
        float_time = hours + (time_in_minutes - hours * 60) / 100
        return float_time

    def set_student(self, student):
        self.student = student

    def set_lesson(self, lesson):
        self.lesson = lesson

    def set_time_of_presence(self, time_of_presence):
        self.time_of_presence = time_of_presence





