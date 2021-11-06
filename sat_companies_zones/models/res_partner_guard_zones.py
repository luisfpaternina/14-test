from odoo import models, fields, api, _

class ResPartnerGuardZones(models.Model):
    _name = 'res.partner.guard.zones'
    _inherit = 'mail.thread'
    _description = 'Guard zone'
    _rec_name = 'code'

    name = fields.Char(
        String="Guard zone name",
        tracking=True)
    code = fields.Char(
        string="Code", 
        tracking=True,
        readonly=True,
        required=True,
        copy=False,
        default='New')
    delegation_id = fields.Many2one(
        'res.partner.delegation',
        string="Delegation",
        tracking=True)
    delegation_name = fields.Char(
        string="Delegation name",
        tracking=True,
        related="delegation_id.name")
    

    # Ejecutar Secuencia 
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('guard.zone') or 'New'
        result = super(ResPartnerGuardZones, self).create(vals)
        return result

    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False
