from odoo import models, fields, api, _
from datetime import datetime
import time
from odoo.exceptions import ValidationError
import logging
logger=logging.getLogger('_______LOGGER B____________')

class hr_employee(models.Model):
   _inherit = 'hr.employee'
   
   gest_course_id = fields.Many2one('gestcal.course',string='Gest cal id')

class GestcalCourse(models.Model):
   
    _name = 'gestcal.course'
    _rec_name = 'name'
    _description = 'Gestcal Course'

    course_id = fields.Char(string='Course id', required=True)
    name = fields.Char(string='Name')
    repetition = fields.Char(string='Repetition')
    total_hours = fields.Float(string='Total Hours')
    topics = fields.Many2many('gestcal.course.topics', string='Theme Areas', readonly=False, store=True)# 'name',
    lesson_ids = fields.One2many('gestcal.lesson', 'course_id', string='Lesson')
    attachments_ids = fields.One2many('gestcal.attachment', 'courses_id', string='Attachment')
    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachment count')
    # courses_ids = fields.Many2one('gestcal.project', string='Courses')
    project_id = fields.Many2one('gestcal.project', string='Project')
    # course_id = fields.Char(string='Course id', required=True)
    teacher_ids = fields.Many2many('res.partner', string='Teacher', domain=[('is_teacher', '=', True)])
    #, 'gest_course_id',##  'gestcal.lesson', 'course_id', 'teacher_ids', 'teacher_id', One2many    teacher_skills = fields.Many2many('gestcal.course.topics', string='Thematic Areas', related='teacher_ids.topics')#, domain=[('is_teacher', '=', True)]
    recipients_ids = fields.Many2many('res.partner', string='Recipients',
                                      domain=[('state', '=', 'active'), ('is_student', '=', True)])



    @api.one
    @api.constrains('repetition')
    def check_repetition(self):
        for record in self:
            repetition_course = self.search([('repetition','=',record.repetition),('id','!=',record.id)])
            if repetition_course:
                raise ValidationError(_("Number of repetition must be unique!"))
        
    # @api.one
    # def get_teachers (self):
    #     teacher_list = []
    #     for rec in self.lesson_ids:
    #         for teacher in rec.teacher_id:
    #             if teacher.id not in teacher_list:
    #                 teacher_list.append(rec.teacher_id.id)
    #     logger.info('__________teacher_list________: %s  ', teacher_list)
    #     self.write({'teacher_ids': [(6, 0, [teacher_list])]})
    #     # self.write(6, 0, [11, 10])
    #     # dictionary = {'teacher_ids': [(6, 0, [teacher_list])]}
    #     # dictionary = {'teacher_ids': [(6, 0, (11, 10))]}
    #     # logger.info('__________dictionary________: %s  ', dictionary.items())
    #     # self.write(dictionary.get('teacher_ids'))
    #     return

    # @api.one
    # def get_recipients(self, context):
    #     recipients_list = []
    #     for rec in self.lesson_ids:
    #         for i in rec.recipients_id:
    #             courses = []
    #             courses.append(context['course_id'])
    #             for i_course_id in i.gest_course_id:
    #                 courses.append(i_course_id)
    #             courses.append(self.get_courses_id_list(i, context['course_id']))#get_course_from_id(context['course_id'])
    #             i.write({'gest_course_id': [(6, 0, courses)]})
    #             if i.id not in recipients_list:
    #                 recipients_list.append(i.id)
    #     logger.info('__________recipients_list________: %s  ', recipients_list)
    #     self.write({'recipients_ids': [(6, 0, recipients_list)]})
    #     return

    @api.one
    def get_recipients (self):
        recipients_list = []
        for recipient in self.recipients_ids:
            recipients_list.append(recipient.id)
        # recipients_list = self.recipients_ids
        # recipients_list = []
        for rec in self.lesson_ids:
            for i in rec.recipients_id:
                if i.id not in recipients_list:
                    recipients_list.append(i.id)
        logger.info('__________recipients_list________: %s  ',recipients_list)
        self.write({'recipients_ids' : [(6,0,recipients_list)]})
        self.set_course()
        return

    @api.one
    def set_course(self):
        course_list = []
        # for index in self.ids:
        #     course_list.append(index)
        course_list.append(self.id)
        for rec in self.recipients_ids:
            for course in rec.gest_course_id:
                if course.id not in course_list:
                    course_list.append(course.id)
            print(self.env['res.partner'].write({'gest_course_id': [
                (6, 0, course_list)]}))  #self.env['res.partner'].  rec.
        for rec in self.lesson_ids:
            rec.get_recipients()
            rec.set_lesson_participations()

            #         course_list.append(rec.id)
        # logger.info('__________course_list________: %s  ', course_list)
        # self.write({'': [(6, 0, course_list)]})
        return

        # def get_course_from_id(self, str_course_id):

    #     for rec in self:
    #         if rec.course_id == str_course_id:
    #             logger.info('__________rec.course_id________: %s  ', rec.course_id)
    #             return rec

    def get_courses_id_list(self, str_course_id, recipient):
        # recipient
        courses_id = []
        courses_id.append(str_course_id)
        for i_course_id in recipient.gest_course_id:
            courses_id.append(i_course_id)
        return courses_id
        # if rec.course_id == str_course_id:
        #     logger.info('__________rec.course_id________: %s  ', rec.course_id)
        #     return rec

    def get_teachers(self):
        teacher_list = []
        for rec in self.lesson_ids:
            if rec.teacher_id.id not in teacher_list:
                teacher_list.append(rec.teacher_id.id)
            logger.info('__________teacher_list________: %s  ', teacher_list)
        self.write({'teacher_ids': [(6, 0, teacher_list)]})
        return
    
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('gestcal.course') or '/'
        vals['repetition'] = seq 
        return super(GestcalCourse, self).create(vals)

 
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

    
class GestcalCourse_topics(models.Model):
   
    _name = 'gestcal.course.topics'
    _description = 'Topic for the Lesson'
    _rec_name = 'name'
    
    name = fields.Char(string='Name', required=True)
    text = fields.Text(string='Text')

    
    