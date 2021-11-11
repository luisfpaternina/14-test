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
    "name": "Norauto Etiquetas Precios",
    "version": "1.0",
    'author': 'Nybble Group',
    "summary": """Etiquetas de Precio""",
    "license": "AGPL-3",
    "depends": ['base', 'fields_norauto', 'norauto_creations'],
    "data": [
        'views/etiqueta_precio_simple.xml',
        'views/etiqueta_precio_promo.xml',
        'views/etiqueta_senalizacion_a6_norauto.xml',
        'views/etiqueta_senalizacion_a6_promo.xml',
        'views/etiqueta_senalizacion_norauto.xml',
        'views/etiqueta_senalizacion_promo.xml',
        'views/product_template_views.xml',
    ],
    'qweb': [],
    "installable": True,
    "active": False,
}
