# -*- coding: utf-8 -*-

import datetime
import stdnum.ar
import xlrd
from datetime import date
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    codigo_proveedor = fields.Integer("Codigo de proveedor",size=7)
    igrbrt = fields.Char("Ingresos Brutos", size=25)
    descuento = fields.Float("DESCUENTO")
    codigo_facturacion = fields.Char("Codigo de Facturacion", size=2)
    condcpa = fields.Char("CONDCPA", size=2)
    imputacml = fields.Integer("IMPUTACML", size=10)
    imputacme = fields.Integer("IMPUTACME", size=10)
    agrupa = fields.Char("AGRUPA")
    retiva = fields.Char("RETIVA", size=1)
    retgan = fields.Char("RETENCION GANANCIAS CATEGORIA", size=1)
    retsus = fields.Char("RETSUS")
    retconstru = fields.Char("RETCONSTRU")
    ordencheq = fields.Char("ORDENCHEQ", size=50)
    codigo_cuit = fields.Char("CODIGOCUIT")
    fecha_alta = fields.Date("Fecha Alta")
    exclusioniva = fields.Char("EXSCLUSIONIVA")
    fecvtoexi = fields.Date("FECVTOEXI")
    exclusiongan = fields.Char("EXCLUSIONGAN")
    fecvtoexg = fields.Date("FECVTOEXG")
    fecinfbco = fields.Date("FECINFBCO")
    formapago = fields.Char("FORMA PAGO")
    cuenta = fields.Char("CUENTA")
    servicios = fields.Char("SERVICIOS")
    fiscal = fields.Char("FISCAL")
    ccostosml = fields.Char("CCOSTOSML")
    ccostosme = fields.Char("CCOSTOSME")
    anegocioml = fields.Char("ANEGOCIOML")
    anegociome = fields.Char("ANEGOCIOME")
    imputacrml = fields.Char("IMPUTACRML")
    imputacrme = fields.Char("IMPUTACRME")
    ccostosrml = fields.Char("CCOSTOSRML")
    ccostosrme = fields.Char("CCOSTOSRME")
    anegociorml = fields.Char("ANEGOCIORML")
    tercermoneda = fields.Char("TERCERMONEDA")
    codpais = fields.Char("CODPAIS")
    rg3164 = fields.Char("RG3164")
    condgan = fields.Char("CONDGAN")
    idtributaria1 = fields.Char("IDTRIBUTARIA1")
    situaciontrib = fields.Char("SITUACIONTRIB")

    revisar_cuit = fields.Boolean("Revisar CUIT")

    @api.model
    def create(self, vals):

        res = super(ResPartner, self).create(vals)

        if res.same_vat_partner_id:
            raise ValidationError('Ya existe un cliente/proveedor con el numero de VAT que asigno. Cambie el numero de VAT para poder darlo de alta.')
        
        return res
        

    ##################################################
    # Metodos auxiliares
    ##################################################
    def carga_proveedores(self):
        """Importa proveedores desde un archivo excel"""
        # NOTE: para que sea mas facil, me bajo la db de produccion, cargo los proveedores aca, y después la restauro en produccion
        # file_location = '/home/androba/proveedores2.xlsx'
        file_location = '/var/lib/odoo/.local/share/Odoo/addons/13.0/addons-norauto/nybble_norauto/fields_norauto/data/proveedores2.xlsx'
        wb = xlrd.open_workbook(file_location)

        suppliers = []
        for sheet in wb.sheets():
            for row in range(2, sheet.nrows):
                supplier_vals = {}
                for cel in range(0, 52):
                    print("row: %s; cell: %s" % (row, cel))
                    supplier_vals[sheet.cell(1, cel).value] = sheet.cell(row, cel).value
                suppliers.append(supplier_vals)

        # import pdb; pdb.set_trace()
        for supplier in suppliers:
            # TODO: convertir campos a tipo aceptado
            supplier['state_id'] = self.get_state_id(supplier['state_id'])
            supplier['country_id'] = self.get_country_id(supplier['country_id'])
            supplier['l10n_ar_afip_responsibility_type_id'] = self.get_responsibility_id(supplier['l10n_ar_afip_responsibility_type_id'])
            supplier['fecha_alta'] = self.xldate_to_string_date(supplier['fecha_alta'])
            supplier['fecvtoexi'] = self.xldate_to_string_date(supplier['fecvtoexi'])
            supplier['fecvtoexg'] = self.xldate_to_string_date(supplier['fecvtoexg'])
            supplier['fecinfbco'] = self.xldate_to_string_date(supplier['fecinfbco'])
            supplier['l10n_latam_identification_type_id'] = 4

            # Si es extranjero o no tiene definido cuit que tipo de documento lleva?
            # TODO: Verificar CUIT
            try:
                stdnum.ar.cuit.validate(supplier['vat'])
            except stdnum.ar.cuit.InvalidChecksum:
                supplier['revisar_cuit'] = True
                supplier['l10n_latam_identification_type_id'] = 3
                # raise ValidationError(_('The validation digit is not valid for "%s"') % rec.l10n_latam_identification_type_id.name)
            except stdnum.ar.cuit.InvalidLength:
                supplier['revisar_cuit'] = True
                supplier['l10n_latam_identification_type_id'] = 3
                # raise ValidationError(_('Invalid length for "%s"') % rec.l10n_latam_identification_type_id.name)
            except stdnum.ar.cuit.InvalidFormat:
                supplier['revisar_cuit'] = True
                supplier['l10n_latam_identification_type_id'] = 3
                # raise ValidationError(_('Only numbers allowed for "%s"') % rec.l10n_latam_identification_type_id.name)
            except Exception as error:
                raise ValidationError(repr(error))

            # TODO: Crear Contactos Auxiliares nope
            # TODO: Crear poner en notas internas
            # TODO: Hacer pop a los auxiliares
            supplier.pop('auxiliar4')
            auxiliares = ['auxiliar1', 'auxiliar2', 'auxiliar3']
            auxiliar_string_list = []
            for auxiliar in auxiliares:
                if supplier[auxiliar] != '':
                    auxiliar_string_list.append(supplier[auxiliar])
                auxiliar_string = ', '.join(auxiliar_string_list)
                print(auxiliar_string)
                supplier['comment'] = auxiliar_string
                supplier.pop(auxiliar)

            # TODO: Agregar supplier rank y otros
            supplier['supplier_rank'] = 1

            # TODO: crear Proveedor
            self.env['res.partner'].create(supplier)

    def xldate_to_string_date(self, xldate):
        if xldate:
            temp = datetime.datetime(1899, 12, 30)
            delta = datetime.timedelta(days=xldate)
            return (temp + delta).strftime("%Y-%m-%d")
        return False

    def get_responsibility_id(self, responsibility_name):
        if responsibility_name:
            responsibilities = {
                'EX': 8,    # Proveedor del Exterior
                'MM': 7,    # Sujeto no categorizado
                'RE': 1,    # Responsable Inscripto
                'RI': 1,    # Responsable Inscripto
                'RM': 6,    # Responsable Monotributo
                'XX': 7,    # Sujeto no categorizado
            }
            return responsibilities[responsibility_name]
        return False

    def get_state_id(self, state_name):
        if state_name:
            states = {
                'CF': 553,
                'BA': 554,
                'CB': 558,
                'EX': False,
                'ME': 565,
                'SF': 573,
                'SL': 571
            }
            return states[state_name]
        return False

    def get_country_id(self, country_name):
        if country_name:
            countries = {
                'Argentina': 10,
                'ARGENTINA': 10,
                'BRASIL': 31,
                'CHINA': 48,
                'HONG KONG': 94,
                'ITALIA': 109,
                'PANAMA': 172,
                'Panama': 172,
                'TAIWAN': 227
            }
            return countries[country_name]
        return False
