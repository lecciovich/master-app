from odoo import models, fields, api, _
from datetime import datetime
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
    start_time = fields.Float(string='Start Time', required=True,digits=(2,2),
                              help='Time according to timeformat of 24 hours')
    end_time = fields.Float(string='End Time', required=True,digits=(2,2),
                            help='Time according to timeformat of 24 hours')
    teacher_id = fields.Many2one('res.partner', string='Teacher' , required=True) # each lession have only ONE teacher
    recipients_id = fields.Many2many('res.partner','lesson_id', string='Recipients') 
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
    @api.constrains('date','start_time','end_time','teacher_id')
    def cheking_lesson(self):
        lesson_obj = self.env['gestcal.lesson']
  
        for rec in lesson_obj.search([]):
            check_less = rec.search([('date' ,'=',self.date),('start_time' ,'=', self.start_time),('end_time' ,'=', self.end_time),('teacher_id' ,'=', self.teacher_id.id)])
            if len(check_less) > 1 :
                raise ValidationError(_('This date already exists for the lesson'))

        
    @api.constrains('start_time','end_time')
    def check_date(self):
        if (self.start_time >= self.end_time):
            logger.info('___________check_date________: %s  ',self.start_time > self.end_time)
            raise ValidationError(_('Start time must be greater than end time !'))

    @api.multi
    @api.depends('date', 'start_time', 'end_time')
    def check_done(self):
        timezone = 2.0
        current_hour = float(datetime.now().strftime("%H.%M")) + timezone
        current_date = datetime.now().date()
        logger.info('___________current_date________: %s  ', current_date)
        logger.info('___________current_hour________: %s  ', current_hour)

        logger.info('___________lesson_date________: %s  ', self.date)
        logger.info('___________start_hour________: %s  ', self.start_time)
        logger.info('___________start_hour________: %s  ', self.end_time)

        sameday_date_check = current_date == self.date
        sameday_hour_check = current_hour > self.end_time
        logger.info('___________check_past_date________: %s  ', sameday_date_check)
        logger.info('___________check_part_hour________: %s  ', sameday_hour_check)
        sameday_check = sameday_date_check and sameday_hour_check

        print("date", sameday_date_check, "hour", sameday_hour_check)
        return sameday_check or current_date > self.date