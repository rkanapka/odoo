# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class BankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.multi
    def button_draft(self):
        self.state = "open"
