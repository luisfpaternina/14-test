from odoo import fields, models, api
import datetime
import pytz
import logging

_logger = logging.getLogger(__name__)

class Producto(models.Model):
    _name = "product.template"
    _inherit = [_name, 'mail.thread', 'mail.activity.mixin']

    es_usuario_pricing = fields.Boolean(compute="_es_usuario_de_pricing")

    precios_venta_ids = fields.One2many(
        string='Precios de venta',
        comodel_name='product.template.historico_cambio_precios',
        inverse_name='product_id',
    )

    precio_anterior = fields.Float(
        string='Precio anterior',
        compute='_obtener_precio_anterior',
        store=True,
        digits=(12, 2)
    )

    precio_a_actualizar_maniana = fields.Float(
        string='Precio a actualizar maniana',
        store=True,
        digits=(12, 2)
    )

    fecha_inicio_actual = fields.Date(
        string='Fecha inicio precio actual',
        compute='_obtener_fecha_precio_actual',
        store=True
    )

    fecha_fin_actual = fields.Date(
        string='Fecha fin precio actual',
        compute='_obtener_fecha_fin_actual',
        store=True
    )

    def actualizar_precio_actual(self):
        dia_local = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).date()
        productos = self.search([('fecha_inicio_actual', '=', dia_local)])
        _logger.info('dia_local: %s' % str(dia_local))
        _logger.info('productos: %s' % str(productos))
        for record in productos:
            _logger.info('record.name: %s' % str(record.name))
            _logger.info('record.fecha_inicio_actual: %s' % str(record.fecha_inicio_actual))
            if record.fecha_inicio_actual == dia_local and record.precio_a_actualizar_maniana > 0:
                record.write({
                    'list_price': record.precio_a_actualizar_maniana,
                    'precio_a_actualizar_maniana': 0
                })


    @api.depends('precios_venta_ids')
    def _obtener_precio_anterior(self):
        if len(self.precios_venta_ids) > 1:
            record_ultimo_precio = self.precios_venta_ids[-2]
            self.precio_anterior = record_ultimo_precio.precio_venta

    @api.depends('precios_venta_ids')
    def _obtener_fecha_precio_actual(self):
        for product in self:
            if len(product.precios_venta_ids) > 0:
                record_ultimo_precio = product.precios_venta_ids[-1]
                product.fecha_inicio_actual = record_ultimo_precio.fecha_inicio

    @api.depends('precios_venta_ids')
    def _obtener_fecha_fin_actual(self):
        for product in self:
            if len(product.precios_venta_ids) > 0:
                record_ultimo_precio = product.precios_venta_ids[-1]
                product.fecha_fin_actual = record_ultimo_precio.fecha_fin

    def _es_usuario_de_pricing(self):
        for record in self:
            record['es_usuario_pricing'] = False
            if self.env.user.has_group('norauto_rights.group_pricing'):
                record['es_usuario_pricing'] = True

    def cambiar_precio_venta(self):
        return {
            'name': 'Generar nueva vigencia de precio de venta',
            'type': 'ir.actions.act_window',
            'res_model': 'update.registro_historico',
            'view_mode': 'form',
            'target': 'new',
            "context": {'articulo': self.id}
        }

    def enviar_notificacion_cambio_precio(self):
        productos = self.search([])
        main_tienda_users = self.env['res.users'].search([]).filtered(lambda r: self.env.user.has_group('norauto_rights.group_tienda'))
        tienda_partners_ids = [u.partner_id.id for u in main_tienda_users]
        self.message_subscribe(partner_ids=tienda_partners_ids, channel_ids=self.message_channel_ids)
        # crear actividad para notificacion
        dia_local = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).date()
        for record in productos:
            if record.fecha_inicio_actual == dia_local:
                summary = "Se ha cambiado un precio del producto %s " % (record.name)
                user = main_tienda_users.filtered(lambda r: r.has_group('norauto_rights.group_tienda') and r.id is not self.env.ref('base.user_admin').id)
                for x in user:
                    self.activity_schedule(act_type_xmlid='mail.mail_activity_data_todo', summary=summary, user_id=x.id)
