# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')


class ResPartner(models.Model):
    _inherit = 'res.partner'
 
    lesson_id = fields.Many2one('gestcal.lesson', 'lesson')
    projects_ids = fields.Many2one('gestcal.project', 'project')
    is_student = fields.Boolean(string='Is a Student?')
    is_teacher = fields.Boolean(string='Is a Teacher?')
    is_operator = fields.Boolean(string='Is a Operator?')

class GestcalProject(models.Model):
 
    _name = 'gestcal.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'
    _description = 'Gestcal project'
    
    title = fields.Char(string='Title', required=True)
    project_code = fields.Char(string='Project code' ,required=True)
    found = fields.Float('Found', required=True)                        # what's the difference between this an financing amount?
    financing_amount = fields.Float('Financing Amount', required=True)  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    total_lesson_hours = fields.Float('Total Lesson Hours') # TODO later on there have to be some non-blocking check that verifies that this value
                                                            # is equal to the sum of the hours of all courses related to the project
    call = fields.Char(string='Call')
    submission = fields.Date(string='Submission')
    admittance = fields.Date(string='Admittance')
    agreement = fields.Date(string='Agreement')
    account_request = fields.Date(string='Account Request')
    partner = fields.Many2many('res.partner','projects_ids', string='Partner')
    deadline = fields.Datetime(string='Deadline')
    courses = fields.Many2many('gestcal.course','courses_ids', string='Courses')
    attachments_ids = fields.One2many('gestcal.attachment', 'projects_id', string='Attachment')
    attachments = fields.Many2one('gestcal.attachment', string='Attachments')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('active', 'Active'), 
        ('completed','Completed'), 
        ('accounted','Sent To Financial Director'), 
        ('closed','Closed')
        
        ], string='Status', index=True, readonly=True, copy=False, default='draft', track_visibility='onchange')

#     @api.multi
#     def _track_subtype(self, init_values):
#         self.ensure_one() 
#         if 'state' in init_values:
#             return 'gest_call.mt_state_change'  # Full external id
#         return super(GestcalProject, self)._track_subtype(init_values)

    def _compute_attachment_count(self):
        for attachment in self: 
            attachment.attachment_count = len(attachment.attachments_ids)
            logger.info('___________count________: %s  ',attachment.attachment_count)
            
    @api.constrains('project_code','title')
    def _check_name(self):
        if self.title ==  self.project_code:
            raise ValidationError(_('Two project Title and Project code can not be the same'))
 
    @api.multi
    def attachment_action_to_open(self):
        ''' This opens the xml view specified in xml_id for the current attachment '''
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')

        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('gest_call', xml_id)
            res.update(
                context={'default_projects_id': self.id,
                         },
                domain=[('projects_id', '=', self.id)]
            )
            logger.info('___________res________: %s  ',res)
            return res
            
        return False

    @api.multi
    def submitted_project(self):
        return self.write({'state': 'submitted'})

    @api.multi
    def active_project(self):
        return self.write({'state': 'active'})

    @api.multi
    def completed_project(self):
        return self.write({'state': 'completed'})

    @api.multi
    def accounted_project(self):
        return self.write({'state': 'accounted'})

    @api.multi
    def closed_project(self):
        return self.write({'state': 'closed'})



class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    
    lesson_id = fields.Many2one('gestcal.lesson', 'lesson')
    is_teacher = fields.Boolean('Is Teacher')

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
    course_id = fields.Many2one('gestcal.course', string='course', required=True)
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
            logger.info('___________date________: %s  ',date,record.date)
            
            date_st = self.search([('start_time','=',record.start_time),('id','!=',record.id)])
            logger.info('___________date_st________: %s  ',date_st)
            
            date_ed = self.search([('end_time','=',record.end_time),('id','!=',record.id)])
            logger.info('___________date_ed________: %s  ',date_ed)
            
            teacher = self.search([('teacher_id','=',record.teacher_id.id),('id','!=',record.id)])
            logger.info('___________teacher________: %s  ',teacher)
              
            if date and date_st and date_ed and teacher: 
                raise ValidationError(_('This date already exists for the lesson'))

    @api.constrains('start_time','end_time')
    def check_date(self):
        if (self.start_time >= self.end_time):
            logger.info('___________check_date________: %s  ',self.start_time > self.end_time)
            raise ValidationError (_('Start time must be greater than end time !')) 
    
class GestcalEquipment(models.Model):

    _name = 'gestcal.equipment'
    _rec_name = 'name'
    _description = 'Gestcal Course equipment' 
    
    name = fields.Char(string='Name')
    number = fields.Integer(string='Number')
    place_id = fields.Many2one('gestcal.place', string='Placeid')

    
class GestcalPlace(models.Model):
 
    _name = 'gestcal.place'
    _rec_name = 'name'
    _description = 'Gestcal Place' 
    
    name = fields.Char(string='Name')
    adress = fields.Char(string='Adress') 
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    seats = fields.Integer (string='Seats')
    equipment = fields.One2many('gestcal.equipment','place_id' ,string='Equipment',
                              help='Related Course equipment') 
    referent = fields.Float('Referent', required=True,
                              help='Time according to timeformat of 24 hours')
    

class GestcalCourse(models.Model):
   
    _name = 'gestcal.course'
    _rec_name = 'name'
    _description = ' Gestcal Course'
    
    name = fields.Char(string='Name')
    repetition = fields.Integer(string='Repetition') # I'm not sure about this field: Repetition should represent the 1st, 2nd, 3rd, etc, repetition of 
                                                     # the same course (so, hours, teacher, title are identical) BUT with DIFFERENT STUDENTS. It's basically ID for the user.
    total_hours = fields.Float(string='Total Hours')
    topics = fields.Char(string='Topics')
    lesson_id = fields.One2many('gestcal.lesson','course_id', string='Lesson') # same of line 48: shouldn't this be One2many? Each course have many lessions date
    attachments_ids = fields.One2many('gestcal.attachment', 'courses_id', string='Attachment')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    courses_ids =  fields.Many2one('gestcal.project', string='courses') 


    def _compute_attachment_count(self):
        for attachment in self:
            attachment.attachment_count = len(attachment.attachments_ids)

    @api.multi
    def attachment_action_to_open(self):
        ''' This opens the xml view specified in xml_id for the current attachment '''
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')

        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('gest_call', xml_id)
            res.update(
                context={'default_courses_id': self.id,
                         },
                domain=[('courses_id', '=', self.id)]
            )
            return res
        
        return False


class GestcalAttachment(models.Model):
   
    _name = 'gestcal.attachment'
    _rec_name = 'name'
    
    name = fields.Char(string='Name')
    description = fields.Char(string='Name')
    validity = fields.Datetime(string='Validity')
    type = fields.Char(string='Type')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachment')
    projects_id = fields.Many2one('gestcal.project', string='projects_id') 
#     contacts_id = fields.Many2one('res.partner', string='contacts_id')
    courses_id = fields.Many2one('gestcal.course', string='courses_id')
#     classrooms_id = fields.Many2one('gestcal.classrooms', string='classrooms_id')

    


    
 