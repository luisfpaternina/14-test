# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MultipleLabels(models.Model):
    _name = 'multiple.labels'
    _inherit = 'mail.thread'
    _description = 'Multiple labels'
