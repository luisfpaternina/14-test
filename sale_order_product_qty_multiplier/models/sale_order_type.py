# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang

from odoo.exceptions import UserError, AccessError, ValidationError

class SaleOrderType(models.Model):
    _inherit = "sale.order.type"


    b2b_type = fields.Boolean('B2B Type')