# -*- coding: utf-8 -*-

from odoo import models, fields, api

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class CourseCalendar(models.Model):
    """Model for course calendar
    """
    _name = 'gestcal.date'
    _description = ""
    _inherit = "calendar.event"
    _order = "" ## Ordering field when searching without an ordering specified (default: 'id') 

    date = fields.Date()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    place = fields.Many2one('gestcal.place') ## (comodel_name=<object object>, inverse_name=<object object>, string=<object object>, **kwargs)
                                              ## comodel c'è, inverse name bisogna fare la classe per le sedi, il resto non so manco cos'è
    beneficiaries = fields.Many2one('res.user')  ## oppure users che beneficiaries è lungo e tedioso
    docent = fields.Many2one('res.user')
    course_module = fields('gestcal.module')


class CourseModule(models.Model):
    """Model for the courses modules in a project
    """
    _name = 'gestcal.coursemod'
    _description = ""
    #_inherit = "" ## anche niente da ereditare
    #_order = "" ## boh

    title = fields.Text()
    #recurrence = ## da decidere cosa fare
    tot_hours = fields.Float()
    courses_date = fields.Many2one('gestcal.date') ## non so cosa sto facendo, sarebbe che ogni edizione potesse avere la view delle date delle lezioni
    ufc = fields.Tex()
    method = fields.Tex()

class Project(models.Model):
    """Model for a project that embodies and tracks all the feature and other
    things that are done as an activity
    """
    _name = 'gestcal.project'
    _description = ""
    # _inherit = ""
    # _order = ""

    