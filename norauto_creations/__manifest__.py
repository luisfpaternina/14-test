# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    All Rights Reserved.
#
############################################################################
#
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Permisos Norauto",
    "version": "1.0",
    'author': 'Nybble Group',
    "summary": """Permisos para Central de Compras, Tienda y Grupos Compradores""",
    "license": "AGPL-3",
    "depends": ['base', 'norauto_rights', 'stock', 'purchase', 'fields_norauto', 'product', 'grupos_compradores'],
    "data": [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/factura.xml',
        'views/pricing.xml',
        'views/purchase_order.xml',
        'views/ocultar_informe_valuacion.xml',
        'views/tabla_historico.xml',
        'views/historico_cambio_precios.xml',
        'views/users.xml',
        'wizards/generar_registro_historico_precios.xml',
        'data/cron_cambio_precio.xml',
        'data/cron_cambiador_precio.xml'
    ],
    'qweb': [],
    "installable": True,
    "active": False,
}
