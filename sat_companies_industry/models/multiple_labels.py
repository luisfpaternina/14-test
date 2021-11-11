# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MultipleLabels(models.Model):
    _name = 'multiple.labels'
    _inherit = 'mail.thread'
    _description = 'Multiple labels'

    label_ids = fields.One2many(
        'multiple.labels.lines',
        'wizard_id',
        string="Gadgets")
    message = fields.Char(
        string="Message")


    def action_print(self):
        for rec in self:
            print("Aqui va el codigo")



class MultipleLabelsLines(models.Model):
    _name = 'multiple.labels.lines'
    _inherit = 'mail.thread'
    _description = 'Multiple labels lines'

    is_selected = fields.Boolean(
        string="Print",
        default=True)
    wizard_id = fields.Many2one(
        'multiple.labels',
        string="Print wizard")
    product_id = fields.Many2one(
        'product.template',
        string="Gadget",
        related="task_id.product_id")
    task_id = fields.Many2one(
        'project.task',
        string="Task")
