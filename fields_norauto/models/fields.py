from odoo import fields, models, api
from odoo.exceptions import AccessError


class Fields(models.Model):
    _inherit = "product.template"
    _name = _inherit

    marca_vehiculo = fields.Char(size=25, string="Marca del vehículo")
    modelo_vehiculo = fields.Char(size=50, string="Modelo del vehículo")
    patente_vehiculo = fields.Char(size=9, string="Patente del vehículo")
    fecha_creacion = fields.Date(
        string="Fecha de creación", default=fields.Date.today(), required=True)
    tipoart_uno = fields.Selection(
        [('Almacenable', 'Almacenable'), ('Consumible', 'Consumible'), ('Servicio', 'Servicio')], string="Tipo", required=True)
    grupo_comprador = fields.Many2one(
        "stock.grupocomp", "Grupo Comprador", related="categ_id.grupo_comprador")
    nomenclatura_prov = fields.Integer(
        string="Nomenclatura del proveedor", required=True)
    clase = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), (
        '7', '7'), ('C', 'C'), ('9', '9')], string="Clase", required=True)
    idart = fields.Integer(string="ID de artículo", required=True)
    tipoart_dos = fields.Selection(
        [("1", 'CCA'), ("2", 'Temporal')], string="Tipo de artículo según origen", required=True)
    # nombre_gondola = fields.Char(size=25, string="Nombre de góndola")
    # id_gondola = fields.Integer(string="ID de góndola")
    # nombre_modulo = fields.Char(size=25, string="Nombre de módulo")
    # nombre_posicion = fields.Char(size=25, string="Nombre de la posición")
    family_code = fields.Char(string="Codigo Familia",
                              help="GM externe columna en biblia de producto")
    vendor_no = fields.Char(string="Código proveedor SAP",
                            help="Fourn. SAP columna en biblia de producto")
    precio_cesion = fields.Float(
        string="Precio de cesión", compute="calcular_precio_cesion")
    es_usuario_CCA = fields.Boolean(compute="_es_usuario_CCA")
    referencia_catalogo = fields.Char(
        string="Referencia Catalogo", help="Ref catalogue columna en biblia de producto")
    supplier_article_num = fields.Char(
        string="Codigo del articulo en proveedor", help="N° article fourn. columna en biblia de producto")
    currency_id = fields.Many2one(
        'res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True)
    rgp_niveluno = fields.Char(
        string="RGP Nivel Uno", related="categ_id.parent_id.parent_id.parent_id.parent_id.name", store=True)
    rgp_niveldos = fields.Char(
        string="RGP Nivel Dos", related="categ_id.parent_id.parent_id.parent_id.name", store=True)
    rgp_niveltres = fields.Char(
        string="RGP Nivel Tres", related="categ_id.parent_id.parent_id.name", store=True)
    rgp_nivelcuatro = fields.Char(
        string="RGP Nivel Cuatro", related="categ_id.parent_id.name", store=True)
    familia = fields.Char(
        string="Familia", related="categ_id.name", store=True)
    acondicionamiento_tienda = fields.Float(
        string='Acondicionamiento tienda', store=True, default=1)
    acondicionamiento_almacen = fields.Float(
        string='Acondicionamiento almacen', store=True, default=1)
    acumulado_impuestos = fields.Float(
        string='Acumulado impuestos', compute='_calcular_acumulado_impuestos', digits=(12,2))
    precio_con_impuestos = fields.Float(
        string='Precio con impuestos', compute='_calcular_precio_con_impuestos', digits=(12,2))
    precio_oculto = fields.Float(
        string='Precio con impuesto interno', compute='_calcular_precio_oculto', store=True)

    @api.onchange('tipoart_dos')
    def convert_to_class_c(self):
        if self.tipoart_dos == "2":
            self.clase = 'C'

    def _es_usuario_CCA(self):
        for record in self:
            record['es_usuario_CCA'] = False
            if self.env.user.has_group('norauto_rights.group_CCA'):
                record['es_usuario_CCA'] = True

    @api.depends('taxes_id')
    def _calcular_acumulado_impuestos(self):

        for record in self:
            if record.taxes_id:
                for impuesto in record.taxes_id:

                    record.acumulado_impuestos += (impuesto.amount *
                                                   record.list_price) / 100
            else:
                record.acumulado_impuestos = 0

    @api.depends('list_price', 'taxes_id')
    def _calcular_precio_oculto(self):

        for record in self:

            record.precio_oculto = record.list_price

            for impuesto in record.taxes_id:

                if impuesto.id == 146:  # id del impuesto interno

                    record.precio_oculto += (record.list_price *
                                             impuesto.amount)/100

    @api.depends('acumulado_impuestos')
    def _calcular_precio_con_impuestos(self):

        for record in self:

            record.precio_con_impuestos = record.acumulado_impuestos + record.list_price

    def calcular_precio_cesion(self):
        margen_cesion = self.env['ir.config_parameter'].sudo(
        ).get_param("margen_cesion")

        for record in self:
            record["precio_cesion"] = record.standard_price
            if (record.tipoart_dos == "1"):
                record["precio_cesion"] = record.standard_price + \
                    (record.standard_price * float(margen_cesion))

    # NOTE: poner type nativo de odoo en consumible como default para que se pueda almacenar

    @api.model
    def create(self, vals):
        vals.update(type='product')
        res = super(Fields, self).create(vals)
        return res

    @api.onchange('tipoart_uno')
    def cambiar_tipo(self):

        if self.tipoart_uno == 'Almacenable':
            self.type = 'product'
        elif self.tipoart_uno == 'Consumible':
            self.type = 'consu'
        elif self.tipoart_uno == 'Servicio':
            self.type = 'service'

    @api.onchange('tipoart_uno')
    def onchange_tipoart_uno(self):

        res = {} 
        if self.tipoart_uno == 'Servicio':
            res['domain'] = {'categ_id': [('parent_id.parent_id.parent_id.parent_id.id', '=', 638)]} #638 es el ID de 2000 EXTERIOR
            
        else:
            res['domain'] = {'categ_id': ["|",["child_id","=",False],["parent_id","ilike",2000]]}
             
        return res
        

    def unlink(self):

        for record in self:
            if record.clase == '9':
                raise AccessError(
                    'Los articulos de clase 9 no pueden ser borrados')

        return super(Fields, self).unlink()
