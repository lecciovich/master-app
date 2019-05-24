from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')



class GestcalLesson(models.Model):

    _name = 'gestcal.lesson'
    _rec_name = 'title'
    _description = 'Gestcal lesson'
#     _inherit = 'calendar.event'

    title = fields.Char(string='Title')
    date = fields.Date(string='Date', required=True)
    start_time = fields.Float('Start Time', required=True,
                              help='Time according to timeformat of 24 hours')
    end_time = fields.Float('End Time', required=True,
                            help='Time according to timeformat of 24 hours')
    teacher_id = fields.Many2one('hr.employee', string='Teacher' , required=True) # each lession have only ONE teacher
    beneficiaries_id = fields.Many2many('res.partner','lesson_id', string='Beneficiaries') # shouldn't this be One2many? One lession has many beneficiaries (or recipients)
    course_id = fields.Many2one('gestcal.course', string='course')
    project_id = fields.Many2one('gestcal.project', string='Project')
    place = fields.Many2one('gestcal.place', string='Place')

#     @api.one 
#     @api.constrains('date','start_time','end_time','teacher_id')
#     def _check_class_semestre_year(self):
#         print ('const')
#         cls=self.env['gestcal.lesson']
#         start = self.start_time
#         end = self.end_time
#         print ('start',start)
#         print ('end',end)
#         check11=cls.search([('start_time','=',self.start_time)])
#         print ('check11',check11)
#         check=cls.search([('date','=',self.date),('start_time','=',self.start_time),('teacher_id','=',self.teacher_id.id)])
#         print ('tt',check)
#         if len(check)>1:
#             raise ValidationError(_('This date already exists'))

    @api.constrains('date','start_time','end_time','teacher_id')
    def cheking_lesson(self): 
  
        for record in self:
            date = self.search([('date','=',record.date),('id','!=',record.id)])
            logger.info('___________date________: %s  ',date)
            
            date_st = self.search([('start_time','=',record.start_time),('id','!=',record.id)])
            logger.info('___________date_st________: %s  ',date_st)
            
            date_ed = self.search([('end_time','=',record.end_time),('id','!=',record.id)])
            logger.info('___________date_ed________: %s  ',date_ed)
            
            teacher = self.search([('teacher_id','=',record.teacher_id.id),('id','!=',record.id)])
            logger.info('___________teacher________: %s  ',teacher)
              
            if date and date_st and date_ed and teacher: 
                print(date,date_st,date_ed,teacher,self.title)
                raise ValidationError(_('This date already exists for the lesson'))

    @api.constrains('start_time','end_time')
    def check_date(self):
        if (self.start_time >= self.end_time):
            logger.info('___________check_date________: %s  ',self.start_time > self.end_time)
            raise ValidationError (_('Start time must be greater than end time !')) 
    