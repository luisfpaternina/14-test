# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartnerAddress(models.Model):
    _name = 'res.partner.address'
    _inherit = 'mail.thread'
    _description = 'DIAN nomenclature'
    _rec_name = 'code'

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

    @api.onchange('name','code')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False
        self.code = self.code.upper() if self.code else False
