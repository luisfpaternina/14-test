from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

letters = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('M', 'M'),
    ('N', 'N'),
    ('L', 'L'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z')
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
    cardinal2_id = fields.Many2one(
        'res.partner.address.cardinals',
        string="Cardinal point")
    number3 = fields.Char(
        string="Number",
        tracking=True)
    letter3 = fields.Selection(letters)
    cardinal3_id = fields.Many2one(
        'res.partner.address.cardinals',
        string="Cardinal point")
    res_partner_city = fields.Many2one(
        'res.partner.city',
        string="City")
    rut = fields.Binary(
        string="Rut",
        tracking=True)
    chamber_commerce = fields.Binary(
        string="Chamber commerce",
        tracking=True)
    data_update = fields.Binary(
        string="Data update / credit application",
        tracking=True)
    rent_last_years = fields.Binary(
        string="Rent last years",
        tracking=True)
    financial_statements = fields.Binary(
        string="Financial statements",
        tracking=True)
    commercial_references = fields.Binary(
        string="Commercial references",
        tracking=True)
    certificate_freedom = fields.Binary(
        string="Certificate of freedom",
        tracking=True)
    establishment_photo = fields.Binary(
        string="Establishment photo",
        tracking=True)


    _sql_constraints = [
        (
            'vat_uniq',
            'UNIQUE (vat)',
            'You can not have two contacts with the same identification number!')
    ]


    @api.onchange(
        'first_name',
        'second_name',
        'last_name',
        'second_last_name')
    def _upper_fields(self):        
        self.first_name = self.first_name.upper() if self.first_name else False
        self.second_name = self.second_name.upper() if self.second_name else False
        self.last_name = self.last_name.upper() if self.last_name else False
        self.second_last_name = self.second_last_name.upper() if self.second_last_name else False


    @api.onchange(
        'nomenclature_id',
        'number1',
        'letter',
        'cardinal_id',
        'number2',
        'letter2',
        'cardinal2_id',
        'number3',
        'letter3',
        'cardinal3_id')
    def _onchange_nombre_completo(self):
        self.complete_address = "%s %s %s %s %s %s %s %s %s %s" % (
            self.nomenclature_id.code if self.nomenclature_id.code else "",
            self.number1 if self.number1 else "",
            self.letter if self.letter else "",
            self.cardinal_id.name if self.cardinal_id.name else "",
            self.number2 if self.number2 else "",
            self.letter2 if self.letter2 else "",
            self.cardinal2_id.name if self.cardinal2_id.name else "",
            self.number3 if self.number3 else "",
            self.letter3 if self.letter3 else "",
            self.cardinal3_id.name if self.cardinal3_id.name else "")


    @api.onchange(
        'first_name',
        'second_name',
        'last_name',
        'second_last_name')
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


    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False


    @api.constrains('phone')
    def check_name(self):
        for rec in self:
            if len(rec.phone) < 6 or re.match(r"^[a-zA-Z][ a-zA-Z]*", rec.phone):
                raise ValidationError(_(
                    'The phone number must be a minimum of 10 characters and cannot contain letters'))
