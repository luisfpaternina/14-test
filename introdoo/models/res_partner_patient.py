# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartnerPatient(models.Model):
    _name = 'res.partner.patient'
    _inherit = 'mail.thread'
    _description = 'Patients'

    name = fields.Char(
        string="Name",
        tracking=True)
    code = fields.Char(
        string="Code",
        tracking=True)
    active = fields.Boolean(
        string="Active",
        tracking=True,
        default=True)
    phone = fields.Char(
        string="Phone",
        tracking=True)
    country_id = fields.Many2one(
        'res.country',
        string="Country")


    @api.onchange('name')
    def _onchange_name(self):
        self.name = self.name.upper() if self.name else False
