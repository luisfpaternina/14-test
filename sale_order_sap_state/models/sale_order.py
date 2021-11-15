# -*- coding: utf-8 -*-
# (C) 2020 Smile (<http://www.smile.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from dateutil import tz
import datetime

from odoo import fields, models, api,_
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class Sale_Order(models.Model):
    _inherit = 'sale.order'

    estado_sap = fields.Selection([('no_suministrado','No Suministrado'),('entregado_parcial','Entregado Parcialmente'),('concluido','Concluido')],'Estado Sap',default='no_suministrado')
    estado_factura_sap = fields.Selection([('invoiced', 'Facturado'),('to_invoice', 'Pendiente para Facturar'),('no_suministrado', 'Pedido No suministrado')], string='Estado Factura SAP',readonly=True,store=True)

    def action_confirm(self):
        resultado=super(Sale_Order, self).action_confirm()
        for linea in self.order_line:
            #Si es servicio, le tildo el campo is_delivery
            if linea.product_id.type=='service':
                linea.write({'is_delivery':True})
            linea.chequear_estados()
        return resultado

    def chequear_estado_entrega(self):
        entregado=True
        for linea in self.order_line.filtered(lambda r: r.is_delivery == False):
            if linea.estado_sap!='concluido':
                self.write({'delivery_status':'to deliver'})
                entregado=False
                break
        if entregado==True:
            self.write({'delivery_status':'delivered'})
#    def write(self,vals):
 #       print('entro a vals:',vals)
  #      if 'invoice_status' in vals:
   #         if vals['invoice_status']=='invoiced':
    #            vals['estado_factura_sap']='invoiced'
     #       elif vals['invoice_status']=='to invoice':
      #          vals['estado_factura_sap']='to_invoice'
       #     else:
        #        vals['estado_factura_sap']='no_suministrado'
#        print('entro a vals fin:',vals)
 #       return super(Sale_Order, self).write(vals)

#    def chequear_estados(self):
 #       print('entro al chequear_estados:',self)
  #      values={}
   #     self.env.cr.execute("select SUM(product_uom_qty),SUM(qty_delivered) from sale_order_line where order_id="+str(self.id))
    #    res = self.env.cr.fetchone()
     #   if res:
            #Cantidad del prod es igual a la cantidad entregada
      #      if res[0]==res[1]:
       #         values['estado_sap']='concluido'
        #    elif res[0]>res[1]:
         #       if res[1]==0:
          #          values['estado_sap']='no_suministrado'
           #     else:
            #        values['estado_sap']='entregado_parcial'
#        if self.invoice_status=='invoiced':
 #           values['estado_factura_sap']='invoiced'
  #      elif self.invoice_status=='to invoice':
   #         values['estado_factura_sap']='to_invoice'
    #    else:
     #       values['estado_factura_sap']='no_suministrado'
      #  print('salgo del chequear_estados:',values)
       # return self.write(values)
      
#    @api.depends('invoice_status')
 #   def _get_estado_factura(self):
  #      for sale in self:
   #         if sale.invoice_status=='invoiced':
    #            sale.estado_factura_sap='invoiced'
     #       elif sale.invoice_status=='to invoice':
      #          sale.estado_factura_sap='to_invoice'
       #     else:
        #        sale.estado_factura_sap='no_suministrado'
