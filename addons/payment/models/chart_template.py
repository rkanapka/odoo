from odoo import api, models


class WizardMultiChartsAccounts(models.TransientModel):
    _inherit = "wizard.multi.charts.accounts"

    @api.multi
    def _create_bank_journals_from_o2m(self, company, acc_template_ref):
        res = super()._create_bank_journals_from_o2m(company, acc_template_ref)

        # Try to generate the missing journals
        return res + self.env["payment.acquirer"]._create_missing_journal_for_acquirers(company=company)
