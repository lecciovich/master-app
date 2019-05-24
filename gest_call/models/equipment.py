from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')



class GestcalEquipment(models.Model):

    _name = 'gestcal.equipment'
    _rec_name = 'name'
    _description = 'Gestcal Course equipment' 
    
    name = fields.Char(string='Name')
    number = fields.Integer(string='Number')
    place_id = fields.Many2one('gestcal.place', string='Placeid')

    