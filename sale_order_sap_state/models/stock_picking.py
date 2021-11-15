# -*- coding: utf-8 -*-

from dateutil import tz
import datetime

from odoo import fields, models, api,_
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def remitir(self):
        print('entro a remitir desde sale_order_sap state')
        res=super(StockPicking, self).remitir()
        if res==True:
            print('entro x true')
            for picking in self:
                if picking.picking_type_id.code == 'incoming' and picking.numero_salida_sap:
                    orden_compra = self.env['purchase.order'].search([('name', '=', picking.origin)])
                    pedidos_sap = orden_compra.numero_pedido_sap.split(',')
                    ordenes_de_venta = self.env['sale.order'].search([('numero_pedido_sap', 'in', pedidos_sap)])
                    for orden in ordenes_de_venta:
                        for linea in orden.order_line:
                            print('entro a chequear')
                            linea.chequear_estados()
        return res
