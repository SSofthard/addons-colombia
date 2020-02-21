# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    is_rte = fields.Boolean(string='IS Rte', default=False,
        help="Check this if the tax is a withholding tax.")
    tax_id = fields.Many2one('account.tax', string='Tax Rte On', ondelete='restrict')

    @api.onchange('is_rte')
    def onchange_is_rte(self):
        if not self.is_rte:
            self.tax_id = False
            
            
