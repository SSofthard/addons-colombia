# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoiceTax(models.Model):
    _inherit = "account.invoice.tax"

    @api.depends('invoice_id.invoice_line_ids')
    def _compute_base_amount(self):
        tax_grouped = {}
        for invoice in self.mapped('invoice_id'):
            tax_grouped[invoice.id] = invoice.get_taxes_values()
        for tax in self:
            tax.base = 0.0
            if tax.tax_id:
                key = tax.tax_id.get_grouping_key({
                    'tax_id': tax.tax_id.id,
                    'account_id': tax.account_id.id,
                    'account_analytic_id': tax.account_analytic_id.id,
                    'analytic_tag_ids': tax.analytic_tag_ids.ids or False,
                })
                if tax.invoice_id and key in tax_grouped[tax.invoice_id.id]:
                    account_tax_id = self.env['account.tax'].search([('id','=',tax_grouped[tax.invoice_id.id][key]['tax_id'])])
                    if account_tax_id and account_tax_id.is_rte:
                        tax_rte_id = account_tax_id.tax_id
                        tax.base = (tax_grouped[tax.invoice_id.id][key]['base'] * tax_rte_id.amount) / 100
                    else:
                        tax.base = tax_grouped[tax.invoice_id.id][key]['base']
                else:
                    _logger.warning('Tax Base Amount not computable probably due to a change in an underlying tax (%s).', tax.tax_id.name)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('invoice_line_tax_ids')
    def onchange_invoice_line_tax_ids(self):
        taxes_rte = []
        taxes_rte_name = []
        taxes_rte_on = []
        for tax in self.invoice_line_tax_ids:
            if tax.is_rte == True:
                taxes_rte.append(tax.id)
                taxes_rte_name.append(tax.name)
                taxes_rte_on.append(tax.tax_id.name)
        if self.invoice_line_tax_ids and self.invoice_line_tax_ids.ids == taxes_rte:
            self.invoice_line_tax_ids = False
            warning = {
                    'title': _('Warning!'),
                    'message': _('Withholding taxes (%s), you must first select the tax to which the withholding applies (%s).') %(", ".join(taxes_rte_name), ", ".join(taxes_rte_on)),
                }
            return {'warning': warning}
        
