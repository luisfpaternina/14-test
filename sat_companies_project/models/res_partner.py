# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.http import request
from odoo.exceptions import ValidationError
import base64
from io import BytesIO


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_potential_client = fields.Boolean(
        string="Is a potential client",
        tracking=True)


    @api.onchange('company_type')
    def _validate_company_type(self):
        for record in self:
            if record.company_type == 'company':
                record.is_potential_client = True
            else:
                record.is_potential_client = False


    @api.constrains('name','is_potential_client')
    def _validate_is_potential_client_identification(self):
        for record in self:
            if record.company_type == 'company':
                if record.is_potential_client != True:
                    if not record.is_oca or record.is_maintainer:
                        if not record.bank_ids:
                            raise ValidationError(_('The bank account field must be filled out'))
            else:
                print("Nothing!")


    @api.constrains('name','is_potential_client')
    def _validate_is_potential_client_vat(self):
        for record in self:
            if record.company_type == 'company':
                if record.is_potential_client != True:
                    if not record.is_oca or record.is_maintainer:
                        if not record.vat:
                            raise ValidationError(_('The identification number field must be filled out'))
            else:
                print('Nothing')


    @api.constrains('name','is_potential_client')
    def _validate_is_potential_client_country(self):
        for record in self:
            if record.company_type == 'company':
                if record.is_potential_client != True:
                    if not record.is_oca or record.is_maintainer:
                        if not record.country_id:
                            raise ValidationError(_('The country field must be filled out'))
            else:
                print('Nothing')


    @api.constrains('name','is_potential_client')
    def _validate_is_potential_client_state(self):
        for record in self:
            if record.company_type == 'company':
                if record.is_potential_client != True:
                    if not record.is_oca or record.is_maintainer:
                        if not record.state_id:
                            raise ValidationError(_('The state field must be filled out'))
            else:
                print('Nothing')


    @api.constrains('name','is_potential_client')
    def _validate_is_potential_client_zip(self):
        for record in self:
            if record.company_type == 'company':
                if record.is_potential_client != True:
                    if not record.is_oca or record.is_maintainer:
                        if not record.zip:
                            raise ValidationError(_('The postal code field must be filled out'))
            else:
                print('Nothing')


    @api.constrains('name','is_potential_client')
    def _validate_is_potential_client_city(self):
        for record in self:
            if record.company_type == 'company':
                if record.is_potential_client != True:
                    if not record.is_oca or record.is_maintainer:
                        if not record.city:
                            raise ValidationError(_('The city field must be filled out'))
            else:
                print('Nothing')
