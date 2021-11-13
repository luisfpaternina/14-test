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
