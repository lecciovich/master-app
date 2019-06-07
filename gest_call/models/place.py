from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')



class GestcalPlace(models.Model):
 
    _name = 'gestcal.place'
    _rec_name = 'name'
    _description = 'Gestcal Place' 
    
    name = fields.Char(string='Name')
    adress = fields.Char(string='Adress') 
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    zip = fields.Char(string='Zip', change_default=True)
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    seats = fields.Integer (string='Seats')
    equipment = fields.One2many('gestcal.equipment','place_id' ,string='Equipment',
                              help='Related Course equipment') 
    referent = fields.Float(string='Referent', required=True,
                              help='Time according to timeformat of 24 hours')

