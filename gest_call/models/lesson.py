from odoo import models, fields, api, _
from datetime import datetime, timedelta
import time
from odoo.exceptions import ValidationError
import logging
import pytz
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
    recipients_id = fields.Many2many('res.partner', 'lesson_id', string='Recipients', domain=[('is_student', '=', True)])#
    course_id = fields.Many2one('gestcal.course', string='course')
    project_id = fields.Many2one('gestcal.project', string='Project',  related='course_id.project_id')
    place = fields.Many2one('gestcal.place', string='Place')

    @api.one
    @api.depends('date', 'start_time')
    def datetime_start_calc(self):
        [_, _, _, user_tz] = self.calc_date_and_time_local(datetime.utcnow())
        # utc_offset = datetime.now(user_tz).utcoffset()
        # tot_min_offset = utc_offset.seconds // 60
        # hour_offset = tot_min_offset // 60
        # float_utc_offset = hour_offset + (tot_min_offset + hour_offset * 60) / 100
        # for rec in self:
        #     print(rec.date)
        #     print(rec.start_time)
        #     logger.info('___________start_time________: %s  ', rec.start_time)
        #     logger.info('___________start_date________: %s  ', rec.date)
        #     # float_utc_start_time = self.set_datetime_given_tz(rec.start_time, user_tz)#rec.start_time - float_utc_offset
        #     # strhour = str(float_utc_start_time)#float_utc_offset
        #     strhour = rec.start_time
        #     logger.info('___________start_time_string________: %s  ', strhour)
        #     strdate = str(rec.date)#.isocalendar()[1]
        print(self.date)
        print(self.start_time)
        logger.info('___________start_time________: %s  ', self.start_time)
        logger.info('___________start_date________: %s  ', self.date)
        # float_utc_start_time = self.set_datetime_given_tz(rec.start_time, user_tz)#rec.start_time - float_utc_offset
        # strhour = str(float_utc_start_time)#float_utc_offset
        # strhour = self.start_time
        # logger.info('___________start_time_string________: %s  ', strhour)
        # strdate = str(self.date)#.isocalendar()[1]
        #
        # logger.info('___________start_date_string________: %s  ', strdate)
        # result_datetime = datetime.strptime(str(strdate) + ' ' + str(strhour), '%YYYY-%mm-%dd %HH.%MM')#.astimezone(user_tz)
        # logger.info('___________start_datetime________: %s  ', result_datetime)
        # # [_, _, current_datetime, _] = self.calc_date_and_time_local(result_datetime)
        # # datetime_local = datetime.strptime(current_datetime, '%Y-%m-%d %H.%M').astimezone(user_tz) #current_date + ' ' + current_hour
        # # logger.info('___________datetime_local________: %s  ', datetime_local)
        # # datetime_local = datetime.strptime(current_date + ' ' + current_datetime, '%Y-%m-%d %H.%M').astimezone(user_tz)
        # current_datetime = self.convert_TZ_UTC(result_datetime, user_tz)
        # logger.info('___________datetime_local________: %s  ', current_datetime)#datetime_local)
        self.date_start_marco = self.from_t_and_d_to_datetime(self.start_time, self.date, user_tz)
            # rec.date_start = current_datetime#datetime_local
        # self.date_start

    @api.one
    @api.depends('date', 'end_time')
    def datetime_end_calc(self):
        [_, _, _, user_tz] = self.calc_date_and_time_local(datetime.utcnow())
        # for rec in self:
        #     print(rec.date)
        #     print(rec.end_time)
        #     logger.info('___________end_time________: %s  ', rec.end_time)
        #     logger.info('___________end_date________: %s  ', rec.date)
        #     strhour = str(rec.end_time)
        #     # float_utc_end_time = self.set_datetime_given_tz(rec.end_time, user_tz)#rec.start_time - float_utc_offset
        #     # strhour = str(float_utc_end_time)#float_utc_offset
        #     logger.info('___________end_time_string________: %s  ', strhour)
        #     strdate = str(rec.date)#.isocalendar()[1]
        print(self.date)
        print(self.end_time)
        logger.info('___________end_time________: %s  ', self.end_time)
        logger.info('___________end_date________: %s  ', self.date)
        # strhour = str(self.end_time)
        # logger.info('___________end_time_string________: %s  ', strhour)
        # strdate = str(self.date)#.isocalendar()[1]
        # logger.info('___________end_date_string________: %s  ', strdate)
        # result_datetime = datetime.strptime(str(strdate) + ' ' + str(strhour), '%YYYY-%mm-%dd %HH.%MM')#.astimezone(user_tz)
        # logger.info('___________end_datetime________: %s  ', result_datetime)
        # # [_, _, current_datetime, _] = self.calc_date_and_time_local(result_datetime)
        # # datetime_local = datetime.strptime(current_date + ' ' + current_datetime, '%Y-%m-%d %H.%M').astimezone(user_tz)
        # current_datetime = self.convert_TZ_UTC(result_datetime, user_tz)
        # logger.info('___________datetime_local________: %s  ', current_datetime)#datetime_local)
        # self.date_start = current_datetime
        self.date_end_marco = self.from_t_and_d_to_datetime(self.end_time, self.date, user_tz)
        # rec.date_start = current_datetime

    def from_t_and_d_to_datetime(self, attr_time, attr_date, tzone):
        strhour = str(attr_time)
        logger.info('___________end_time_string________: %s  ', strhour)
        strdate = str(attr_date)  # .isocalendar()[1]
        logger.info('___________end_date_string________: %s  ', strdate)
        result_datetime = datetime.strptime(str(strdate) + ' ' + str(strhour), '%Y-%m-%d %H.%M')  # .astimezone(user_tz)
        logger.info('___________end_datetime________: %s  ', result_datetime)
        # [_, _, current_datetime, _] = self.calc_date_and_time_local(result_datetime)
        # datetime_local = datetime.strptime(current_date + ' ' + current_datetime, '%Y-%m-%d %H.%M').astimezone(user_tz)
        current_datetime = self.convert_TZ_UTC(result_datetime, tzone)
        logger.info('___________datetime_local________: %s  ', current_datetime)#datetime_local)
        return current_datetime
    #     @api.constrains('date','start_time','end_time','teacher_id')
#     def cheking_lesson(self): 
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
    def checking_lesson(self):
        lesson_obj = self.env['gestcal.lesson']
  
        for rec in lesson_obj.search([]):
            check_less = rec.search([('date' ,'=',self.date),('start_time' ,'=', self.start_time),('end_time' ,'=', self.end_time),('teacher_id' ,'=', self.teacher_id.id)])
            if len(check_less) > 1 :
                raise ValidationError(_('This date already exists for the lesson'))

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
        #
        print('datetime today', datetime_today)
        print('date today', current_date)
        print('time today', current_hour)
        print('user tz: ', user_tz)
        # date_today = pytz.utc.localize(my_datetime_field).astimezone(user_tz)

        # timezone = 2.0
        # current_hour = float(datetime.now().strftime("%H.%M"))+timezone
        # current_date = datetime.now().date()

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
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        datetime_local = datetime_arg.astimezone(user_tz)
        date_local = datetime_local.date()#.isoformat()
        time_local = datetime.time(datetime_local)#.strftime("%H.%M")
        # datetime_local.utcoffset().seconds
        return date_local, time_local, datetime_local, user_tz

    def set_datetime_given_tz(self, local_time, tzone):
        # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        # datetime_local = datetime.__setattr__(date,date)
        # datetime.now(tzone).utcoffset().seconds
        float_tzone = self.translate_seconds_to_float_time(datetime.utcoffset(tzone).seconds)
        utc_time = local_time - float_tzone
        return utc_time
        #
        # date_local = datetime_local.date()  # .isoformat()
        # time_local = datetime.time(datetime_local)  # .strftime("%H.%M")
        # return datetime_timezoned

    def trasform_time_in_float(self, datetime_time):
        logger.info('___________current_date_hour________: %s  ', datetime_time.hour)
        logger.info('___________current_date_hour_from_minute________: %s  ', datetime_time.minute//60)
        logger.info('___________current_date_minute________: %s  ', datetime_time.minute - datetime_time.minute//60)
        # float_hour = datetime_time.hour + datetime_time.minute // 60
        # float_min = (datetime_time.minute - 60 * (datetime_time.minute // 60)) / 100
        # float_time = float_hour + float_min
        tot_seconds = datetime_time.hour * 3600 + datetime_time.minute * 60
        float_time = self.translate_seconds_to_float_time(tot_seconds)
        return float_time



    def sum_duration(self, duration1, duration2):
        sum_minutes = duration1 * 100 + duration2 * 100
        # float_hour = sum_minutes // 60
        # float_min = (sum_minutes - 60 * float_hour) / 100
        # sum_time = float_hour + float_min
        sum_time = self.translate_seconds_to_float_time(sum_minutes * 60)
        return sum_time

    def translate_seconds_to_float_time(self, time_in_seconds):
        time_in_minutes = time_in_seconds // 60
        hours = time_in_minutes // 60
        float_time = hours + (time_in_minutes - hours * 60) / 100
        return float_time

    def saveandcreate(self, cr, uid, ids, context=None):
        return True

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