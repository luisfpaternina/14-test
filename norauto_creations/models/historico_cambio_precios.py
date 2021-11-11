from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date

class HistoricoCambioPrecios(models.Model):
    _name = 'product.template.historico_cambio_precios'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'product_id'

    fecha_inicio = fields.Date(
        string='Fecha de inicio'
    )

    fecha_fin = fields.Date(
        string='Fecha de fin'
    )

    usuario_id = fields.Many2one(
        string='Usuario',
        comodel_name='res.users',
        default=lambda self: self.env.user.id
    )

    precio_venta = fields.Float(
        string='Precio de venta',
        # related='product_id.list_price'
    )

    product_id = fields.Many2one('product.template', string="Producto", ondelete='cascade')

    @api.model
    def create(self, vals):
        res = super(HistoricoCambioPrecios, self).create(vals)
        res.product_id.write({'precio_a_actualizar_maniana': res.precio_venta})
        return res

    def enviar_notificacion_expiracion_precio(self):
        main_tienda_users = self.env['res.users'].search([]).filtered(lambda r: self.env.user.has_group('norauto_rights.group_tienda'))
        tienda_partners_ids = [u.partner_id.id for u in main_tienda_users]
        self.message_subscribe(partner_ids=tienda_partners_ids, channel_ids=self.message_channel_ids)
        # crear actividad para notificacion
        for record in self:
            summary = "Ha expirado el precio de venta del producto %s. Por favor genere una nueva vigencia para el mismo." % (record.product_id.name)
            user = main_tienda_users.filtered(lambda r: r.has_group('norauto_rights.group_tienda') and r.id is not self.env.ref('base.user_admin').id)
            if (record.fecha_fin == date.today()):
                for x in user:
                    record.activity_schedule(act_type_xmlid='mail.mail_activity_data_todo', summary=summary, user_id=x.id)
                    record.message_post(body=message)
