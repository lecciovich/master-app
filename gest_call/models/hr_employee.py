from odoo import models, fields, api, _

   
class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    
    lesson_id = fields.Many2one('gestcal.lesson', 'Lessons')
    is_teacher = fields.Boolean('Is Teacher')

