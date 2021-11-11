# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MultipleLabels(models.Model):
    _name = 'multiple.labels'
    _inherit = 'mail.thread'
    _description = 'Multiple labels'











class MultipleLabelsLines(models.Model):
    _name = 'multiple.labels.lines'
    _inherit = 'mail.thread'
    _description = 'Multiple labels lines'

    is_selected = fields.Boolean(
        string="Print")
    wizard_id = fields.Many2one(
        'multiple.labels',
        string="Print wizard")
