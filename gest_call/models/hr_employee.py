from odoo import models, fields, api, _

   
class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    _rec_name = 'name'
    
    lesson_id = fields.Many2one('gestcal.lesson', 'Lessons')
    is_teacher = fields.Boolean('Is Teacher')
    topics = fields.Many2many('gestcal.course.topics', string='Topics')
#
#
# class Topic(models.Model):
#
#     _name = 'hr.topic'
#     _rec_name = 'title'
#
#     title= fields.Char("Title")
#
