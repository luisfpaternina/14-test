from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import *


class OrdenDeCompra(models.Model):

    _inherit = "purchase.order"
    grupo_comprador_usuario = fields.Many2one('stock.grupocomp', "Grupo Comprador de Usuario")
    state = fields.Selection(selection_add=[('aprobacion_finanzas', 'A aprobar por finanzas'), ('aprobacion_central_compras', 'A aprobar por Central de Compras')])
    creado_por_tienda = fields.Boolean('Creado en tienda', default=False)

    @api.model
    def create(self, vals):
        if self.env.user.has_group('norauto_rights.group_tienda'):
            vals['creado_por_tienda'] = True
        else:
            vals['creado_por_tienda'] = False

        if self.env.user.es_gestioo == False:
            if self.env.user.has_group('norauto_rights.group_tienda') and self.env.user.has_group('norauto_rights.group_CCA'):
                raise ValidationError(
                    "Permiso Denegado. Usted como usuario no puede tener el permiso de tienda y central de compras habilitado a la vez, porfavor comuniquese con su administrador")
        res = super(OrdenDeCompra, self).create(vals)
        return res

    def write(self, vals):
        if self.env.user.has_group('norauto_rights.group_tienda') and \
                not self.env.user.has_group('norauto_rights.group_CCA') and \
                not self.creado_por_tienda and \
                not self.env.context.get('confirmar'):
            raise ValidationError("Permiso Denegado. No puede editar la orden de compra una vez aprobada. Si desea editar la orden por favor comuníquese con Central de Compras")

        if self.env.user.es_gestioo == False:
            if self.env.user.has_group(
                    'norauto_rights.group_tienda') and self.env.user.has_group(
                'norauto_rights.group_CCA'):
                raise ValidationError(
                    "Permiso Denegado. Usted como usuario no puede tener el permiso de tienda y central de compras habilitado a la vez, porfavor comuniquese con su administrador")
        res = super(OrdenDeCompra, self).write(vals)
        return res

    def verificar_grupo_comprador(self):

        grupos_compradores = self.obtener_grupos_compradores()

        articulos_no_en_grupo_comprador = []
        grupo_comprador_user = 0

        for rec in self:
            for linea in rec.order_line:
                for x in grupos_compradores:
                    grupo = 'norauto_rights.group_gc%d_abm' % x

                    if not self.env.user.has_group(grupo) and linea.product_id.grupo_comprador.number == x:
                        articulos_no_en_grupo_comprador.append(linea.product_id.name.rstrip())
                        continue
                    else:
                        if not grupo_comprador_user:
                            grupo_comprador_user = x
                        break

        if len(articulos_no_en_grupo_comprador) > 0:
                    
            raise ValidationError(("Permiso denegado. Agregó los artículos: " + str(articulos_no_en_grupo_comprador) + ", que no pertenecen a su grupo comprador " + str(grupo_comprador_user)))
                
        self.grupo_comprador_usuario = self.env['stock.grupocomp'].search([('number', '=', grupo_comprador_user)]).id

    def verificar_pedido_urgente(self):

        cumple_validacion = False

        if self.partner_id == self.env["res.partner"].search([('name', '=', 'Pedidos Urgentes')]):
            if self.env.user.has_group("norauto_rights.group_tienda"):
                cumple_validacion = True
            else:
                raise ValidationError("Permiso denegado. Solo usuarios de Tienda pueden generar órdenes de compra a Pedidos Urgentes.")

        return cumple_validacion

    def segunda_validacion(self):
        if self.env.user.has_group('norauto_creations.norauto_group_finanzas_aprobacion_ordenes'):
            # self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
            self.with_context({'aprobado_finanzas': True}).button_approve()
        else:
            raise ValidationError(
                "Solo los usuarios con el permiso 'Finanzas aprobación ordenes "
                "de compra' tienen permitido ejecutar esta acción")

    def button_confirm(self):
        #import pdb; pdb.set_trace()
        res = super(OrdenDeCompra, self).button_confirm()
        if self.verificar_pedido_urgente():
            self.write({'state': 'purchase'})
        elif self.env.user.has_group('norauto_rights.group_tienda') and self.creado_por_tienda:
            self.with_context({'confirmar': True}).write({'state': 'aprobacion_central_compras'})
        else:
            self.verificar_grupo_comprador()
            self.write({'state': 'to approve'})
        #self.is_shipped = True

        return res

    def button_approve(self):
        # Si es usuario gestioo pasa siempre sin importar nada
        if self.env.user.es_gestioo:
            res = super(OrdenDeCompra, self).button_approve()
            return res

        if self.env.context.get('aprobado_finanzas', False):
            res = super(OrdenDeCompra, self).button_approve()
            return res

        if self.state != "draft":
            if (self.env.user.has_group("norauto_rights.group_gerente_compras")):
                if (self.verificar_tope_mensual()):
                    self.write({'state': 'aprobacion_finanzas'})
                else:
                    self.write({'state': 'purchase'})
                    res = super(OrdenDeCompra, self).button_approve()
                    return res
            else:
                raise ValidationError("Usted no es Gerente de Compras (No posee privilegios de Administrador en Compras)")

    def button_cancel(self):

        res = super(OrdenDeCompra, self).button_cancel()

        self.verificar_grupo_comprador()

        return res

    def button_confirm_central_compras(self):
        self.write({'state': 'purchase'})

    def verificar_tope_mensual(self):
        # for j in range(1, 10, 1):
        #     exec('grupo_{0} = {0}'.format(j))
        #
        # for j in range(1, 10, 1): print("var_{0} = {0}".format(j))
        # ordenes_compra_mes_actual = self.env['purchase.order'].search(
        #     []).filtered(
        #     lambda r: self.filtrar_por_mes(r.date_order, datetime.now().month))
        # for orden in ordenes_compra_mes_actual:
        #     for linea in orden.order_line:
        #         grupo_comprador: linea.product_id.product_tmpl_id.grupo_comprador
        grupos_compradores = []
        for linea in self.order_line:
            # exec('grupo_{0} = {0}'.format(linea.product_id.product_tmpl_id.grupo_comprador.id))
            grupos_compradores.append(linea.product_id.product_tmpl_id.grupo_comprador.id)
        lineas_ordenes_compra = self.env['purchase.order.line'].search([("product_id.product_tmpl_id.grupo_comprador.id", "in", list(set(grupos_compradores)))])
        lineas_ordenes_compra_mes_actual = lineas_ordenes_compra.filtered(lambda r: self.filtrar_por_mes(r.order_id.date_order, datetime.now().month))
        total_mes = 0
        excede_limite = False
        for grupo in list(set(grupos_compradores)):
            for orden in lineas_ordenes_compra_mes_actual.filtered(lambda r: r.product_id.product_tmpl_id.grupo_comprador.id == grupo):
                total_mes += orden.acuerdo_subtotal
                if total_mes > self.env['stock.grupocomp'].browse(grupo).limite_segunda_aprobacion:
                    excede_limite = True
                return excede_limite

    def obtener_grupos_compradores(self):
        grup_comp = self.env["stock.grupocomp"].search([])

        grupos_compradores = []

        for x in grup_comp:
            grupos_compradores.append(x.number)

        return grupos_compradores

    def filtrar_por_mes(self, mes_orden, mes_actual):
        coincidencia = False
        mes_pasado = datetime.now() - relativedelta(months=1)  # en caso de que la orden se haya hecho el último día del mes, obtengo el mes pasado
        if mes_orden.month == mes_actual or mes_orden.month == mes_pasado.month:
            coincidencia = True
        return coincidencia
