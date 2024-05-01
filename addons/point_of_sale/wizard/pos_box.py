# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.account.wizard.pos_box import CashBox

from odoo import _, api
from odoo.exceptions import UserError


class PosBox(CashBox):
    _register = False

    @api.multi
    def run(self):
        active_model = self.env.context.get("active_model", False)
        active_ids = self.env.context.get("active_ids", [])

        if active_model == "pos.session":
            bank_statements = [
                session.cash_register_id
                for session in self.env[active_model].browse(active_ids)
                if session.cash_register_id
            ]
            if not bank_statements:
                raise UserError(_("There is no cash register for this PoS Session"))
            return self._run(bank_statements)
        else:
            return super().run()


class PosBoxIn(PosBox):
    _inherit = "cash.box.in"

    def _calculate_values_for_statement_line(self, record):
        values = super()._calculate_values_for_statement_line(record=record)
        active_model = self.env.context.get("active_model", False)
        active_ids = self.env.context.get("active_ids", [])
        if active_model == "pos.session" and active_ids:
            values["ref"] = self.env[active_model].browse(active_ids)[0].name
        return values


class PosBoxOut(PosBox):
    _inherit = "cash.box.out"

    def _calculate_values_for_statement_line(self, record):
        values = super()._calculate_values_for_statement_line(record)
        active_model = self.env.context.get("active_model", False)
        active_ids = self.env.context.get("active_ids", [])
        if active_model == "pos.session" and active_ids:
            values["ref"] = self.env[active_model].browse(active_ids)[0].name
        return values
