# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectTaskOtChecklist(models.Model):
    _name = 'project.task.ot.checklist'
    _inherit = 'mail.thread'
    _description = 'OT checklist'

    name = fields.Char(
        string="Name",
        tracking=True)
    location = fields.Char(
        string="Location",
        tracking=True)
    accomplished = fields.Selection([
        ('yes','Yes'),
        ('Not','Not')],string="Accomplished", tracking=True)
    code = fields.Char(string="Code")
    check_1 = fields.Boolean(string="1ª")
    check_2 = fields.Boolean(string="2ª")
    check_3 = fields.Boolean(string="3ª")
    check_4 = fields.Boolean(string="4ª")
    check_5 = fields.Boolean(string="5ª")
    check_6 = fields.Boolean(string="6ª")
    check_7 = fields.Boolean(string="7ª")
    check_8 = fields.Boolean(string="8ª")
    check_9 = fields.Boolean(string="9ª")
    check_10 = fields.Boolean(string="10ª")
    check_11 = fields.Boolean(string="11ª")
    check_12 = fields.Boolean(string="12ª")
    line_number = fields.Char(
        string="N° line",
        readonly=True,
        required=True,
        copy=False,
        default='New')
    location_id = fields.Many2one(
        'project.task.ot.checklist.location',
        string="Location")
    user_id = fields.Many2one(
        'res.users',
        string="Operator")
    task_id = fields.Many2one(
        'project.task',
        string="Task")
    month_date = fields.Char(
        string="Month",
        compute="calculate_month")


    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False


    # Ejecutar Secuencia 
    @api.model
    def create(self, vals):
        if vals.get('line_number', 'New') == 'New':
            vals['line_number'] = self.env['ir.sequence'].next_by_code('checklist') or 'New'
        result = super(ProjectTaskOtChecklist, self).create(vals)
        return result


    @api.depends('create_date')
    def calculate_month(self):
        for record in self:
            dt = datetime.datetime.today()
            record.month_date = dt.month
