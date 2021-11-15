# -*- coding: utf-8 -*-

from dateutil import tz
import datetime

from odoo import fields, models, api,_
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

from odoo.exceptions import UserError, AccessError, ValidationError, Warning


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        if self.product_id and self.product_id.qty_multiplier>0:
            if self._origin and self._origin.order_id.type_id.b2b_type:
                if self.product_uom_qty % self.product_id.qty_multiplier != 0.0:
                    self._origin.order_id.write({'qty_multiplier_info':True})
                    return {
                        'warning': {
                            'title': 'Avertencia!',
                            'message': 'Cantidad del empaquetado no es correcto, debe ser multiplo de '+str(self.product_id.qty_multiplier)}
                    }
                else:
                    self._origin.order_id.write({'qty_multiplier_info':False})


    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.product_id.qty_multiplier>0:
            if self.order_id.type_id.b2b_type:
                if self.product_uom_qty % self.product_id.qty_multiplier != 0.0:
                    if self._origin.order_id:
                        self._origin.order_id.write({'qty_multiplier_info':True})
                    return {
                        'warning': {
                            'title': 'Avertencia!',
                            'message': 'Cantidad del empaquetado no es correcto, debe ser multiplo de '+str(self.product_id.qty_multiplier)}
                    }
                else:
                    self.order_id.write({'qty_multiplier_info':False})
                
