# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
 
    lesson_id = fields.Many2one('gestcal.lesson', 'lesson')
    projects_ids = fields.Many2one('gestcal.project', 'project')
    is_student = fields.Boolean(string='Is a Student?')
    is_teacher = fields.Boolean(string='Is a Teacher?')
    is_operator = fields.Boolean(string='Is a Operator?')
    
    gest_course_id = fields.Many2one('gestcal.course',string='gest cal id')
  

    
 