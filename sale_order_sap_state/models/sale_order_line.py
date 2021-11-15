# -*- coding: utf-8 -*-

from dateutil import tz
import datetime

from odoo import fields, models, api,_
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    estado_sap = fields.Selection([('no_suministrado','No Suministrado'),('entregado_parcial','Entregado Parcialmente'),('concluido','Concluido')],'Estado Sap',default='no_suministrado',readonly=True,store=True,compute='_get_estado_sap')
    estado_factura_sap = fields.Selection([('invoiced', 'Facturado'),('to_invoice', 'Pendiente para Facturar'),('no_suministrado', 'Pedido No suministrado')], string='Estado Factura SAP',readonly=True,store=True,compute='_get_estado_factura')

    def write(self,vals):
        print('entro a vals:',vals)
        if 'invoice_status' in vals:
            if vals['invoice_status']=='invoiced':
                vals['estado_factura_sap']='invoiced'
            elif vals['invoice_status']=='to invoice':
                vals['estado_factura_sap']='to_invoice'
            else:
                vals['estado_factura_sap']='no_suministrado'
        print('entro a vals fin:',vals)
        return super(SaleOrderLine, self).write(vals)

    def chequear_estados(self):
        print('entro al chequear_estados:',self)
        values={}
        if self.is_delivery==False:
            self.env.cr.execute("select SUM(product_uom_qty),SUM(qty_delivered) from sale_order_line where id="+str(self.id))
            res = self.env.cr.fetchone()
            print('res:',res)
            if res:
                #Cantidad del prod es igual a la cantidad entregada
                if res[0]==res[1]:
                    values['estado_sap']='concluido'
                elif res[0]>res[1]:
                    if res[1]==0:
                        values['estado_sap']='no_suministrado'
                    else:
                        values['estado_sap']='entregado_parcial'
            if self.invoice_status=='invoiced':
                values['estado_factura_sap']='invoiced'
            elif self.invoice_status=='to invoice':
                values['estado_factura_sap']='to_invoice'
            else:
                values['estado_factura_sap']='no_suministrado'
            print('salgo del chequear_estados:',values)
        else:
            values['estado_sap']='concluido'
            if self.invoice_status=='invoiced':
                values['estado_factura_sap']='invoiced'
            elif self.invoice_status=='to invoice':
                values['estado_factura_sap']='to_invoice'
            else:
                values['estado_factura_sap']='no_suministrado'
        res=self.write(values)
        self.order_id.chequear_estado_entrega()
        return res 

    @api.depends('product_uom_qty','qty_delivered')
    def _get_estado_sap(self):
        for record in self:
            if type(record.id) == int:
                if record.is_delivery==False:
                    self.env.cr.execute("select SUM(product_uom_qty),SUM(qty_delivered) from sale_order_line where id="+str(record.id))
                    res = self.env.cr.fetchone()
                    if res:
                        #Cantidad del prod es igual a la cantidad entregada
                        if res[0]==res[1]:
                            record.estado_sap='concluido'
                        elif res[0]>res[1]:
                            if res[1]==0:
                                record.estado_sap='no_suministrado'
                            else:
                                record.estado_sap='entregado_parcial'
                else:
                    record.estado_sap='concluido'
            else:
                record.estado_sap='no_suministrado'

    @api.depends('invoice_status')
    def _get_estado_factura(self):
        for record in self:
            if record.invoice_status=='invoiced':
                record.estado_factura_sap='invoiced'
            elif record.invoice_status=='to invoice':
                record.estado_factura_sap='to_invoice'
            else:
                record.estado_factura_sap='no_suministrado'
