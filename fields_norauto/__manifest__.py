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
    "name": "Alta de artículos",
    "version": "1.0",
    'author': 'Nybble Group',
    "summary": """Modificación de alta de artículos para Norauto""",
    "license": "AGPL-3",
    "depends": ['stock', 'base', 'grupos_compradores', 'l10n_ar', 'l10n_ar_pos_einvoice_ticket', 'purchase'],
    "data": [
        'views/fields_view.xml',
        'views/button_view.xml',
        'views/res_partner_view.xml',
        

    ],
    'qweb': [],
    "installable": True,
    "active": False,
}
