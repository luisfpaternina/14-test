from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('phone')
    def validate_phone(self):
        for rec in self:
            if rec.phone:
                if len(rec.phone) < 6 or re.match(r"^[a-zA-Z][ a-zA-Z]*", rec.phone):
                    raise ValidationError('El número de télefono no puede contener letras')
