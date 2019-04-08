# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class newmod(models.Model):
#     _name = 'newmod.newmod'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class CourseCalendar(models.Model):
    """Model for course calendar

    """
    _name = 'GestCal.course'
    _description = ""
    _inherit = "calendar.event"
    _order = "" ## Ordering field when searching without an ordering specified (default: 'id') prova prova

    proj = fields.Many2one()
    



# CAMPI
# data (datetime)
# ora inizio (datetime/float)
# ora fine (datetime/float)
# sede (string/ ref sedi?)
# ** destinatari (ref anagrafe)
# ** modulo (ref moduli)
# ** docente (ref contatto)
