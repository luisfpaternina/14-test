# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_external = fields.Boolean(
        string="Is external",
        tracking=True)
    sale_type_id = fields.Many2one(
        'sale.order.type',
        string="Sale type",
        tracking=True)
    oportunity_type_id = fields.Many2one(
        'crm.lead.type',
        string="Oportunity type")
    client_type = fields.Selection(
        [('neighborhood_community','Neighborhood community'),
        ('companies','Companies/builders'),
        ('public_organisms','Public organisms'),
        ('family_home','Single-family private homes')],string="Client type")
    managed_by = fields.Selection([
        ('president','President'),
        ('admin','Administrator')],string="Managed by")
    is_medium_website = fields.Boolean(
        string="Website medium",
        compute="_compute_check_medium_id")


    @api.depends('medium_id')
    def _compute_check_medium_id(self):
        for record in self:
            record.is_medium_website = True if record.medium_id and record.medium_id[0].name  == 'Website' else False
    