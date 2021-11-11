from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductosNoTemporales(models.Model):
    _inherit = ["product.template"]

    @api.model
    def create(self, vals):
        res = super(ProductosNoTemporales, self).create(vals)
        for record in self:
            record.cca_checking(record)

        return res

    def write(self, vals):
        res = super(ProductosNoTemporales, self).write(vals)
        for record in self:
            record.cca_checking(record)
        return res

    def unlink(self):
        res = super(ProductosNoTemporales, self).unlink()

        for record in self:
            self.cca_checking(record)

        return res

    def cca_checking(self, item):
        if not self.env.user.has_group('norauto_rights.group_creacion_supresion_modificacion_CCA') and item.tipoart_dos == "1":
            raise ValidationError(
                ("Permiso denegado. Usted no tiene permisos de creacion, supresion y modificacion para CCA."))
