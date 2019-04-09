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

    projcode = fields.Text()
    fund = fields.Many2one('gestcal.fund') ## da vedere se fare un oggetto esterno o una stringa baucca
    financed = fields.Float()
    course_hours = fields.Integer()
    internal_hours = fields.Integer()
    dgr = fields.Text()
    presentation_date = fields.Date()
    # notify_date = fields.Date()
    # convention_date = fields.Date()
    finish_date = fields.Date() ## data che va computata in base alle regole della dgr/fondo in cui il progetto è stato presentato
    acconto_date = fields.Date() ## data che va computata in base a diversi fattori, quindi nel costruttore va prevista una funzione che la calcola in base al fondo e alla dgr in cui il progetto è stato presentato
    attachments = fields.Selection([]) ##lista (vuota) di allegati, issue#2 capire cosa usare
    holder = fields.Many2one('res.user')  ##io contunuo a usare res.user ma non so se va bene
    partners = fields.Many2many('res.user')  ##io contunuo a usare res.user ma non so se va bene
    users = fields.Many2many('res.user')  ##io contunuo a usare res.user ma non so se va bene
    # corsi = ??? # non so ancora cosa c'è qua: come si rappresentano i corsi di un progetto? ==> ogni corso è un'edizione di un singolo modulo formativo
    policy = fields.Text()
    # operators = ??? ## potrebbero essere in un dizionario tipo {ruolo:res.user,...} in cui ruolo può essere o una stringa che specifica il ruolo o un oggetto se è il caso di avere un oggetto ma non credo
    