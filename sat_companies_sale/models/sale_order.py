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
    type_contract = fields.Selection([
        ('normal','Normal'),
        ('risk','All risk')],string="Contract type")
    is_create_task = fields.Boolean(
        string="Create task",
        tracking=True,
        related="sale_type_id.is_create_task")
    check_contract_type = fields.Boolean(
        compute="_compute_check_contract_type",
        )
    type_service_id = fields.One2many(
        'sale.check.type.contract',
        'order_id',
        string='Type service'
        )
    delegation_id = fields.Many2one(
        'res.partner.delegation',
        string="Delegation")
    

    @api.depends('sale_type_id')
    def _compute_check_contract_type(self):
        for record in self:
            record.type_contract = False
            if record.sale_type_id.code == '01':
                record.check_contract_type = True
            else:
                record.check_contract_type = False


    @api.constrains('contract_line_ids')
    def _check_exist_record_in_lines(self):
        for rec in self:
            exis_record_lines = []
            for line in rec.contract_line_ids:
                if line.contact_id.id in exis_record_lines:
                    raise ValidationError(_(
                        'The item should be one per line'))
                exis_record_lines.append(line.contact_id.id)

    @api.onchange('type_service_id')
    def get_item_count(self):
        for rec in self:
            count = 1
            for line in rec.type_service_id:
                line.item = count
                count += 1

    def get_table_type_contracts(self):

        flag = False
        table = '<ul>'
        for  type_service_id in self.type_service_id:
            flag = True
            table += '<li>' + str(type_service_id.type_service_id.name) + '  </li>'
        
        table += '</ul>'
        return table if flag else False