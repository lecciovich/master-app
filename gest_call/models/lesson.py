from odoo import models, fields, api, _
from datetime import datetime, timedelta
import time
import pytz
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')

class GestcalLesson(models.Model):

    _name = 'gestcal.lesson'
    _rec_name = 'date'
    _description = 'Gestcal lesson'
#     _inherit = 'calendar.event'

    date = fields.Date(string='Date', required=True)
    # start_time = fields.Datetime(string='Start Time')
    # end_time = fields.Datetime(string='End Time')
    start_time = fields.Float(string='Start Time', required=True,digits=(2,2),
                              help='Time according to timeformat of 24 hours')
    end_time = fields.Float(string='End Time', required=True,digits=(2,2),
                            help='Time according to timeformat of 24 hours')
    teacher_id = fields.Many2one('res.partner', string='Teacher', required=True, domain=[('is_teacher', '=', True)]) # each lession have only ONE teacher
    recipients_id = fields.Many2many('res.partner', 'lesson_id', string='Recipients', domain=[('is_student', '=', True)])
    course_id = fields.Many2one('gestcal.course', string='course')
    project_id = fields.Many2one('gestcal.project', string='Project',  related='course_id.project_id')
    place = fields.Many2one('gestcal.place', string='Place')


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

        sameday_date_check = fields.Date(current_date) == self.date
        sameday_hour_check = self.trasform_time_in_float(current_hour) > self.end_time #float(current_hour)
        logger.info('___________check_past_date________: %s  ', sameday_date_check)
        logger.info('___________check_part_hour________: %s  ', sameday_hour_check)
        sameday_check = sameday_date_check and sameday_hour_check

        print("date", sameday_date_check, "hour", sameday_hour_check)
        return sameday_check or current_date > self.date


    def get_now_date_and_time_local(self):
        return self.calc_date_and_time_local(datetime.utcnow())

    def calc_date_and_time_local(self, datetime_arg):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        datetime_local = datetime_arg.astimezone(user_tz)
        date_local = datetime_local.date()#.isoformat()
        time_local = datetime.time(datetime_local)#.strftime("%H.%M")
        return date_local, time_local, date_local, user_tz

    def trasform_time_in_float(self, datetime_time):
        # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        #if datetime_time is fields.Datetime:
        # datetime.now().m
        # datetime_time.day * 24 +
        logger.info('___________current_date_hour________: %s  ', datetime_time.hour)
        logger.info('___________current_date_hour_from_minute________: %s  ', datetime_time.minute//60)
        logger.info('___________current_date_minute________: %s  ', datetime_time.minute - datetime_time.minute//60)
        float_hour = datetime_time.hour + datetime_time.minute // 60
        float_min = (datetime_time.minute - 60 * (datetime_time.minute // 60)) / 100
        float_time = float_hour + float_min
        return float_time

    def sum_duration(self, duration1, duration2):
        sum_minutes = duration1 * 100 + duration2 * 100
        float_hour = sum_minutes // 60
        float_min = (sum_minutes - 60 * float_hour) / 100
        sum_time = float_hour + float_min
        return sum_time
