from odoo import fields, models, api

class ImpuestoPorLineaFactura(models.Model):

    _inherit = 'account.move'
    _name = _inherit

    impuestos_ids = fields.Many2many(
        string='Impuestos por linea',
        comodel_name='account.tax'
    )

    @api.onchange('impuestos_ids')
    def cargar_impuestos(self):

        impuestos = []
        lineas = []

        for impuesto in self.impuestos_ids:

            impuestos.append(impuesto.id)

        for linea in self.invoice_line_ids:

            lineas.append((1, linea.id, {'tax_ids': [(6,0,impuestos)]}))

        self.invoice_line_ids = lineas

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id', 'impuestos_ids')
    def _compute_invoice_taxes_by_group(self):
        res = super(ImpuestoPorLineaFactura, self)._compute_invoice_taxes_by_group()
        print("amount group", self.amount_by_group)
        return res
