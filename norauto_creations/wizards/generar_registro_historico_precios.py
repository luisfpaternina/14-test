from odoo import models, fields
from odoo.exceptions import UserError, ValidationError
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class GenerarRegistroWizard(models.TransientModel):
    _name = "update.registro_historico"
    _description = "Asignar detalles para el nuevo precio del articulo"
    
    new_precio_venta = fields.Float(
        string='Nuevo precio de venta',
    )

    new_fecha_inicio = fields.Date(string="Nueva fecha de inicio")
    
    new_fecha_fin = fields.Date(string="Nueva fecha de fin")

    def guardar_registro(self):

        if self.new_fecha_inicio == date.today():
            raise UserError ('No puede seleccionar a la fecha actual como la fecha nueva de vigencia.')

        if self.new_fecha_inicio > self.new_fecha_fin:
            raise UserError ('La fecha de inicio no puede ser posterior a la fecha de fin.')

        if self.new_fecha_fin == date.today():
            raise UserError ('No puede seleccionar a la fecha actual como la nueva fecha de fin.')
        
        historico = self.env['product.template.historico_cambio_precios']

        producto = self.env['product.template'].search([('id', '=', self.env.context.get("articulo"))])
        producto.sudo().write({
            'precio_a_actualizar_maniana': self.new_precio_venta
        })

        historico.create({
            'fecha_inicio': self.new_fecha_inicio,
            'fecha_fin': self.new_fecha_fin,
            'usuario_id': self.env.uid,
            'precio_venta': self.new_precio_venta,
            'product_id': self.env.context.get("articulo")
        })

        

    
