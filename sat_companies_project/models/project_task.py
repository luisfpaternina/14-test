from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request
from .qr_code_base import generate_qr_code
import base64
from io import BytesIO
import qrcode

class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'
    
    ##QR SCANNER FIELDS##
    qr_scanner = fields.Char(
        'Qr Scanner')
    state_check_qr = fields.Selection([
        ('checking','Checking'),
        ('done','Done')],string="State Check Gagdest", default='checking', tracking=True)
    delegation = fields.Many2one(
        'res.partner.delegation',
        string="Delegation")
    from_gadget = fields.Many2one(
        'stock.gadgets',
        string="From the Gadget")
    to_gadget = fields.Many2one(
        'stock.gadgets',
        string="To the Gadget")
    from_zone = fields.Many2one(
        'res.partner.zones',
        string="From the Zone")
    to_zone = fields.Many2one(
        'res.partner.zones',
        string="To the Zone")
    delegation_location = fields.Char(
        string="Name",
        related='delegation.name')
    from_gadget_location = fields.Char(
        string="Name",
        related='from_gadget.name')
    to_gadget_location = fields.Char(
        string="Name",
        related='to_gadget.name')
    from_zone_location = fields.Char(
        string="Name",
        related='from_zone.name')
    to_zone_location = fields.Char(
        string="Name",
        related='to_zone.name')
    qr_scanner = fields.Char(
        String = 'Qr Scanner')
    check_pit = fields.Boolean(
        String = 'Pit', tracking=True)
    check_cabine = fields.Boolean(
        String = 'Cabine', tracking=True)
    check_machine = fields.Boolean(
        String = 'Machine', tracking=True)
    qr_pit = fields.Binary(
        'Dowload Qr Image Pit',
        compute="_generate_qr_code")
    qr_pit_image = fields.Binary(
        'QR CODE IMAGE PIT',
        compute="_generate_qr_code")
    qr_cabine = fields.Binary(
        'Dowload QR Image Cabine',
        compute="_generate_qr_code")
    qr_cabine_image = fields.Binary(
        'QR CODE IMAGE CABINE',
        compute="_generate_qr_code")
    qr_machine = fields.Binary(
        'Dowload QR Image Machine',
        compute="_generate_qr_code")
    qr_machine_image = fields.Binary(
        'QR CODE IMAGE MACHINE',
        compute="_generate_qr_code")
    check_qr_active = fields.Boolean(
        'Check Qr')
    pit_confirm = fields.Boolean(
        'Pit confirm')
    cabin_confirm = fields.Boolean(
        'Cabine confirm')
    machine_confirm = fields.Boolean(
        'Machine confirm')


    def confirm_check_gadget(self):
        for record in self:
            if record.qr_scanner:
                if 'pit' in record.qr_scanner or 'machine' in record.qr_scanner or 'cabine' in record.qr_scanner:
                    scanner_value = record.qr_scanner.split(",")
                    gadget_value = scanner_value[0]
                    id_task = int(scanner_value[1])
                    domain = ('id','=',id_task)
                    project_task = self.env['project.task'].search([domain])
                    for task in project_task:
                        if gadget_value == 'pit':
                            task.check_pit = True
                            record.pit_confirm = True
                            record.cabin_confirm = False
                            record.machine_confirm = False
                            record.qr_scanner = False
                        elif gadget_value == 'machine':
                            task.check_machine = True
                            record.pit_confirm = False
                            record.cabin_confirm = False
                            record.machine_confirm = True
                            record.qr_scanner = False
                        elif gadget_value == 'cabine':
                            task.check_cabine = True
                            record.pit_confirm = False
                            record.cabin_confirm = True
                            record.machine_confirm = False
                            record.qr_scanner = False
    

    @api.onchange('qr_scanner')
    def _onchange_qr_scanner(self):
        for record in self:
            if record.qr_scanner:
                record.check_qr_active = True
            else:
                record.check_qr_active = False


    def write(self, vals):
        res = super(ProjectTaskInherit, self).write(vals)
        for record in self:
            if 'check_pit' in vals or 'check_cabine' in vals or 'check_machine' in vals :
                if record.check_pit == True and record.check_cabine == True and record.check_machine == True:
                    record.state_check_qr = 'done'
                else:
                    record.state_check_qr = 'checking'


    def _generate_qr_code(self):
        for record in self:
            if record.product_id:
                base_url_pit = "pit,%d" % (record.id)
                base_url_cabine = "cabine,%d" % (record.id)
                base_url_machine = "machine,%d" % (record.id)
                record.qr_pit = generate_qr_code(base_url_pit)
                record.qr_pit_image = generate_qr_code(base_url_pit)
                record.qr_cabine = generate_qr_code(base_url_cabine)
                record.qr_cabine_image = generate_qr_code(base_url_cabine)
                record.qr_machine = generate_qr_code(base_url_machine)
                record.qr_machine_image = generate_qr_code(base_url_machine)
            else:
                record.qr_pit = False
                record.qr_pit_image = False
                record.qr_cabine = False
                record.qr_cabine_image = False
                record.qr_machine = False
                record.qr_machine_image = False


    def action_url(self):
        return {  
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type'     : 'ir.actions.act_url',
            'target'   : 'self',
            'url'      : self.qr_scanner
            }
