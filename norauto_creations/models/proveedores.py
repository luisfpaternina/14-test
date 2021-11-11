from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Proveedores(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        res = super(Proveedores, self).create(vals)
        if self.supplier_rank >	0:
            if not self.env.user.has_group('norauto_rights.group_CCA'):
                raise ValidationError(("Permiso denegado. Usted no pertenece a Central de Compras"))
        
        return res
      
    def write(self,vals):
        res = super(Proveedores,self).write(vals)
        if self.supplier_rank >	0:
            if not self.env.user.has_group('norauto_rights.group_CCA'):
                raise ValidationError(("Permiso denegado. Usted no pertenece a Central de Compras"))
        return res

    def unlink(self):
        for record in self: 
            if record.supplier_rank > 0:
                if not record.env.user.has_group('norauto_rights.group_CCA'):
                    raise ValidationError(("Permiso denegado. Usted no pertenece a Central de Compras"))
        rec = super(Proveedores,self).unlink()

        return rec

        







   
