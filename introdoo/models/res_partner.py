from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'
