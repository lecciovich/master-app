# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError


# class res_partner(models.Model):
#     _inherit = 'res.partner'


class GestcalProject(models.Model):
 
    _name = 'gestcal.project'
    _rec_name = 'title'
    _description = "Gestcal project"
    
    title = fields.Char(string="Title", required=True)
    project_code = fields.Char(string="Project code" ,required=True)
    found = fields.Float('Found', required=True)                        # what's the difference between this an financing amount?
    financing_amount = fields.Float('Financing Amount', required=True)  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    total_lesson_hours = fields.Float('Total Lesson Hours') # TODO later on there have to be some non-blocking check that verifies that this value
                                                            # is equal to the sum of the hours of all courses related to the project
    call = fields.Char(string="Call")
    submission = fields.Datetime(string="Submission")
    admittance = fields.Datetime(string="Admittance")
    agreement = fields.Datetime(string="Agreement")
    account_request = fields.Datetime(string="Account Request")
    partner = fields.Many2one('res.partner', string="Partner")
    deadline = fields.Datetime(string="Deadline")
    courses = fields.Many2one('gestcal.course', string="Courses")
    

class GestcalLesson(models.Model):
 
    _name = 'gestcal.lesson'
    _rec_name = 'title'
    _description = "Gestcal lesson"
#     _inherit = "calendar.event"

    title = fields.Char(string="Title", required=True)
    date = fields.Date(string="Date")
    start_time = fields.Float('Start Time', required=True,
                              help="Time according to timeformat of 24 hours")
    end_time = fields.Float('End Time', required=True,
                            help="Time according to timeformat of 24 hours")
    beneficiaries_id = fields.Many2one('hr.employee', string="Beneficiaries") # shouldn't this be One2many? One lession has many beneficiaries (or recipients)
    teacher_id = fields.Many2one('hr.employee', string="Teacher") # each lession have only ONE teacher

class GestcalEquipment(models.Model):
   
    _name = 'gestcal.equipment'
    _rec_name = 'name'
    _description = "Gestcal Course equipment" 
    
    name = fields.Char(string="Name")
    number = fields.Integer(string="Number")
    place_id = fields.Many2one('gestcal.place', string="Placeid")

    
class GestcalPlace(models.Model):
 
    _name = 'gestcal.place'
    _rec_name = 'name'
    _description = "Gestcal Place" 
    
    name = fields.Char(string="Name")
    adresse = fields.Char(string="Adresse") 
    seats = fields.Integer (string="Seats")
    equipment = fields.One2many('gestcal.equipment','place_id' ,string="Equipment",
                              help="Related Course equipment") 
    referent = fields.Float('Referent', required=True,
                              help="Time according to timeformat of 24 hours")
    

class GestcalCourse(models.Model):
   
    _name = 'gestcal.course'
    _rec_name = 'name'
    _description = " Gestcal Course"
    
    name = fields.Char(string="Name")
    repetition = fields.Integer(string="Repetition") # I'm not sure about this field: Repetition should represent the 1st, 2nd, 3rd, etc, repetition of 
                                                     # the same course (so, hours, teacher, title are identical) BUT with DIFFERENT STUDENTS. It's basically ID for the user.
    total_hours = fields.Float(string="Total Hours")
    topics = fields.Char(string='Topics')
    lesson_id = fields.Many2one('gestcal.lesson', string="Lesson") # same of line 48: shouldn't this be One2many? Each course have many lessions date

 