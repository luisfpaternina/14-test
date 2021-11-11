from odoo import fields, models, api

class TotalInventario(models.Model):
    _inherit = 'stock.quant'

    @api.depends('company_id', 'location_id', 'owner_id', 'product_id', 'quantity')
    def _compute_value(self):

        res = super(TotalInventario, self)._compute_value()

        for record in self:
            
            if record.location_id != self.env['stock.location'].browse(8): # 8 es el ID del Main Warehouse
                record.write({
                    'value': record.quantity * record.product_id.precio_cesion
                })
            else:
                return res
