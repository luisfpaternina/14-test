from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    unimes = fields.Char(string="Unidad de medida etiqueta")
    nbrunimes = fields.Float(string="nbrunimes")
    precio_uni_med = fields.Float(string="Precio por Unidad de Medida", store=True, compute='_compute_precio_uni_med')

    formated_date = fields.Char(string="Fecha formateada", store=True, compute='_compute_formate_date')

    @api.depends('nbrunimes', 'precio_con_impuestos')
    def _compute_precio_uni_med(self):
        for producto in self:
            if producto.nbrunimes:
                producto.precio_uni_med = round(producto.precio_con_impuestos/producto.nbrunimes, 2)

    @api.depends('fecha_inicio_actual')
    def _compute_formate_date(self):
        for producto in self:
            if producto.fecha_inicio_actual:
                dia = str(producto.fecha_inicio_actual.strftime("%d"))
                mes = str(producto.fecha_inicio_actual.strftime("%m"))
                anno = str(producto.fecha_inicio_actual.strftime("%y"))
                format_date = str(dia + ' ' + mes)
                format_date_2 = str(format_date + ' ' + anno)
                producto.formated_date = format_date_2
            else:
                producto.formated_date = ''
