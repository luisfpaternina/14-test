# -*- coding: utf-8 -*-
from typing import DefaultDict
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_type_id = fields.Many2one(
        'sale.order.type',
        string="Sale type",
        tracking=True)
    is_potential_client = fields.Boolean(
        string="Is a potential client",
        tracking=True,
        related="partner_id.is_potential_client")
    

    def get_task_sale_type(self):
        if self.sale_type_id:
            order_type_form = self.env.ref('sat_companies_project.wizard_sale_order_type_form',raise_if_not_found=False)
            ctx = dict(
                default_name = str(self.name +' - '+ self.partner_id.name),
                default_model='wizard.sale.order.type',
                default_sale_order_id=self.id,
                default_sale_type_id=self.sale_type_id.id,
            )
            return {
                'name': ('Tipo de operación'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.sale.order.type',
                'views': [(order_type_form.id, 'form')],
                'view_id': order_type_form.id,
                'context': ctx,
                'target': 'new',
                }
        else:
            self.action_confirm()

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.is_potential_client:
            raise ValidationError(_("Verify the type of client if it is potential"))
            return res
