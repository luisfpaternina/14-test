# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    address = fields.Char(
        string="Address",
        related="partner_id.street",
        tracking=True)
    population_id = fields.Many2one(
        'res.partner.population',
        string="Population",
        tracking=True)
    sale_type = fields.Selection([
        ('maintenance','Maintenance'),
        ('mounting','Mounting'),
        ('repair','Repair')],string="Sale type")
    is_create_task = fields.Boolean(
        string="Create task",
        tracking=True,
        related="sale_type_id.is_create_task")


    @api.constrains('contract_line_ids')
    def _check_exist_record_in_lines(self):
        for rec in self:
            exis_record_lines = []
            for line in rec.contract_line_ids:
                if line.contact_id.id in exis_record_lines:
                    raise ValidationError(_(
                        'The item should be one per line'))
                exis_record_lines.append(line.contact_id.id)
