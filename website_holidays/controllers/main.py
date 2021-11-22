from odoo import http
from odoo.http import request


class HrHolidays(http.Controller):
    @http.route('/holidays_webform', type="http", auth="public", website=True)
    def holidays_webform(self, **kw):
        leave_type_rec = request.env['hr.leave.type'].sudo().search([])
        return http.request.render('website_holidays.create_holidays', {'leave_type_rec': leave_type_rec,})

    @http.route('/create/webholidays', type="http", auth="public", website=True)
    def create_webholidays(self, **kw):
        request.env['hr.leave'].sudo().create(kw)
        return request.render("website_holidays.holidays_thanks", {})
