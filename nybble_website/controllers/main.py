from odoo import http
from odoo.http import request

class Patient(http.Controller):
    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):
        ticket_type_rec = request.env['helpdesk.ticket.type'].sudo().search([])
        return http.request.render('nybble_website.create_patient', {})


    @http.route('/create/webpatient', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        request.env['helpdesk.ticket'].sudo().create(kw)
        return request.render("nybble_website.patient_thanks", {})
