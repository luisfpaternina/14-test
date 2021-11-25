from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import re

class ResCompany(models.Model):
    _inherit = 'res.company'

    terms = fields.Text(string="Terminos y condiciones")
