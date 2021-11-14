from odoo import http
from odoo.http import request


class Patient(http.Controller):
    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):
        return http.request.render('introdoo.create_patient', {})

    @http.route('/create/webpatient', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        request.env['res.partner.patient'].sudo().create(kw)
        countries = request.env['res.country'].sudo().search([])
        return request.render("introdoo.patient_thanks", {})
