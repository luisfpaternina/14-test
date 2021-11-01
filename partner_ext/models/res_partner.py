from odoo import models, fields, api

letters = [
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
    ('f', 'F'),
    ('g', 'G'),
    ('h', 'H'),
    ('i', 'I'),
    ('j', 'J'),
    ('k', 'K'),
    ('m', 'M'),
    ('n', 'N'),
    ('l', 'L'),
    ('o', 'O'),
    ('p', 'P'),
    ('q', 'Q'),
    ('r', 'R'),
    ('s', 'S'),
    ('t', 'T'),
    ('u', 'U'),
    ('v', 'V'),
    ('w', 'W'),
    ('x', 'X'),
    ('y', 'Y'),
    ('z', 'Z')
]

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_state = fields.Selection([
        ('contact','Contact'),
        ('verification','Verification'),
        ('third_accountant','Third accountant')], string="State",default="contact")
    first_name = fields.Char(
        string="First name",
        tracking=True)
    second_name = fields.Char(
        string="Second name",
        tracking=True)
    last_name = fields.Char(
        string="Last name",
        tracking=True)
    second_last_name = fields.Char(
        string="Second last name",
        tracking=True)
    fullname = fields.Char(
        string="Full name",
        tracking=True)
    is_colombia = fields.Boolean(
        string="Is colombia",
        compute="_compute_check_country_id")
    nomenclature_id = fields.Many2one(
        'res.partner.address',
        string="Nomenclature")
    cardinal_id = fields.Many2one(
        'res.partner.address.cardinals',
        string="Cardinal point")
    number1 = fields.Char(
        string="Number",
        tracking=True)
    letter = fields.Selection(letters)
    complete_address = fields.Char(
        string="Complete address DIAN",
        tracking=True)
    number2 = fields.Char(
        string="Number",
        tracking=True)
    letter2 = fields.Selection(letters)


    @api.onchange('first_name','second_name','last_name','second_last_name')
    def _upper_fields(self):        
        self.first_name = self.first_name.upper() if self.first_name else False
        self.second_name = self.second_name.upper() if self.second_name else False
        self.last_name = self.last_name.upper() if self.last_name else False
        self.second_last_name = self.second_last_name.upper() if self.second_last_name else False


    @api.onchange('nomenclature_id','number1','letter','cardinal_id')
    def _onchange_nombre_completo(self):
        self.complete_address = "%s %s %s %s" % (
            self.nomenclature_id.code if self.nomenclature_id.code else "",
            self.number1 if self.number1 else "",
            self.letter if self.letter else "",
            self.cardinal_id.name if self.cardinal_id.name else "")


    @api.onchange('first_name', 'second_name', 'last_name', 'second_last_name')
    def _onchange_complete_address(self):
        if self.company_type == 'person':
            self.first_name = self.first_name.upper() if self.first_name else False
            self.second_name = self.second_name.upper() if self.second_name else False
            self.last_name = self.last_name.upper() if self.last_name else False
            self.second_last_name = self.second_last_name.upper() if self.second_last_name else False
            self.name = "%s %s %s %s" % (
                self.first_name if self.first_name else "",
                self.second_name if self.second_name else "",
                self.last_name if self.last_name else "",
                self.second_last_name if self.second_last_name else "")


    @api.onchange('name')
    def _compue_fullname(self):
        if self.company_type == 'person':
            self.fullname = self.name
        else:
            print("Es una compañia")


    @api.depends('country_id')
    def _compute_check_country_id(self):
        for record in self:
            record.is_colombia = True if record.country_id and record.country_id[0].name  == 'Colombia' else False
