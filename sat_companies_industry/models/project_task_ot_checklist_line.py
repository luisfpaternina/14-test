# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import datetime
import logging


class ProjectTaskOtChecklistLine(models.Model):
    _name = 'project.task.ot.checklist.line'
    _inherit = 'mail.thread'
    _description = 'OT checklist line'

    name = fields.Char(
        string="Name",
        tracking=True)
    task_id = fields.Many2one(
        'project.task',
        string="Task",
        tracking=True)
    minute_point_id = fields.Many2one(
        'maintenance.minute.point',
        string="Minute point",
        tracking=True)
    type_deffect_id = fields.Many2one(
        'maintenance.type.deffect',
        string="Type of deffect",
        tracking=True,
        related="minute_point_id.type_deffect_id")
    is_reviewed = fields.Boolean(
        string="Is reviewed")
    minute_point_description = fields.Text(
        string="Description",
        related="minute_point_id.description")
    checklist_id = fields.Many2one(
        'project.task.ot.checklist',
        string="Checklist")
    is_reviewed_checklist = fields.Boolean(
        string="Is reviewed")
    month_date = fields.Char(
        string="Month",
        compute="calculate_month")


    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False


    @api.depends('create_date')
    def calculate_month(self):
        for record in self:
            dt = datetime.datetime.today()
            record.month_date = dt.month


    @api.onchange('checklist_id')
    def onchange_checklist(self):
        logging.info('*******************************************************')
        checklist_obj = self.env['project.task.ot.checklist'].search([])
        check_ids = []
        a = []
        for check in checklist_obj:
            if check.check_11 == True and check.month_date == '11':
                check_ids.append(check.id)
        if check_ids:
            logging.info('##########################################')
            logging.info(check_ids)
            return {'domain':{'checklist_id':[('ids', '=', check_ids)]}}
