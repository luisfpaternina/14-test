from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductosTemporales(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals):
        res = super(ProductosTemporales, self).create(vals)

        for record in self:

            self.tienda_checking(record)

        return res

    def write(self, vals):
        res = super(ProductosTemporales, self).write(vals)
        for record in self:

            self.tienda_checking(record)

        return res


    def unlink(self):
        res = super(ProductosTemporales, self).unlink()
        for record in self:
            self.tienda_checking(record)

        return res

    def tienda_checking(self, item):
        if not self.env.user.has_group('norauto_rights.group_creacion_supresion_modificacion_tienda') and item.tipoart_dos == "2":
            raise ValidationError(
                ("Permiso denegado. Usted no tiene permisos de creacion, supresion y modificacion para tienda."))
