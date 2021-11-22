from odoo import models, fields, api, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    priority = fields.Selection(
    selection=[
        ('0', 'Todos'),
        ('1', 'Prioridad baja'),
        ('2', 'Alta prioridad'),
        ('3', 'Urgente'),
        ('4', 'Bloqueante'),
    ],
)
