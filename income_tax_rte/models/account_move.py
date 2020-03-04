# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

#----------------------------------------------------------
# Calculate Tax Base Amount in Journal Entries
#----------------------------------------------------------

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends('move_id.line_ids', 'move_id.line_ids.tax_line_id', 'move_id.line_ids.debit', 'move_id.line_ids.credit')
    def _compute_tax_base_amount(self):
        for move_line in self:
            if move_line.tax_line_id:
                base_lines = move_line.move_id.line_ids.filtered(lambda line: move_line.tax_line_id in line.tax_ids and move_line.partner_id == line.partner_id)
                tax_rte_id = move_line.tax_line_id.tax_id
                if move_line.tax_line_id.is_rte and move_line.tax_line_id.tax_id:
                    move_line.tax_base_amount = (abs(sum(base_lines.mapped('balance'))) * tax_rte_id.amount) / 100
                else:
                    move_line.tax_base_amount = abs(sum(base_lines.mapped('balance')))
            else:
                move_line.tax_base_amount = 0
