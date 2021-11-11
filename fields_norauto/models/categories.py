from odoo import fields, models

class Categories(models.Model):

    _inherit = 'product.category'

    def name_get(self):
        res = []

        for rec in self:
            res.append((rec.id, rec.name))
        
        return res