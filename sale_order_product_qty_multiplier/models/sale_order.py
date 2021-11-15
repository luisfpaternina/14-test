# -*- coding: utf-8 -*-

from dateutil import tz
import datetime

from odoo import fields, models, api,_
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    qty_multiplier_info = fields.Boolean(
        string='QTY Multiplier Info',
    )

    def write(self, values):
        if values.get('order_line'):
            if self.type_id and self.type_id.b2b_type:
                for line in self.order_line:
                    if line.product_uom_qty % line.product_id.qty_multiplier != 0.0:
                        values['qty_multiplier_info']=True
        res=super(SaleOrder, self).write(values)
        return res


    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('order_line'):
            if self.type_id and self.type_id.b2b_type:
                for line in self.order_line:
                    if line.product_uom_qty % line.product_id.qty_multiplier != 0.0:
                        values['qty_multiplier_info']=True
        result = super(SaleOrder, self).create(values)
        return result
    