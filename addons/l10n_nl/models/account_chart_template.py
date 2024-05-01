from odoo import api, models


class WizardMultiChartsAccounts(models.TransientModel):
    _inherit = "wizard.multi.charts.accounts"

    @api.multi
    def execute(self):
        # Add tag to 999999 account
        res = super().execute()
        account = self.env["account.account"].search(
            [("code", "=", "999999"), ("company_id", "=", self.company_id.id)]
        )
        if account:
            account.tag_ids = [(4, self.env.ref("l10n_nl.account_tag_12").id)]
        return res
