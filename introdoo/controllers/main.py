from odoo import http
from odoo.http import request


class Patient(http.Controller):
    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):
        countries_rec = request.env['res.country'].sudo().search([])
        return http.request.render('introdoo.create_patient', {})

    @http.route('/create/webpatient', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        request.env['res.partner.patient'].sudo().create(kw)
        return request.render("introdoo.patient_thanks", {})
