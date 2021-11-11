from odoo import fields, models, api

class Class9Button(models.Model):
    _inherit = 'product.template'
    _description = 'Botón para convertir a clase 9'
    
    @api.depends('qty_available')
    def class_nine_convert(self):

        self.purchase_ok = False
        self.clase = '9'

        if (self.qty_available == 0):
            self.active = False
    
