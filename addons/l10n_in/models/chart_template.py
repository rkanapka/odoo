# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    @api.multi
    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        res = super()._prepare_all_journals(acc_template_ref, company, journals_dict=journals_dict)
        if not self == self.env.ref("l10n_in.indian_chart_template_standard"):
            return res
        for journal in res:
            if journal["code"] == "INV":
                journal["name"] = _("Tax Invoices")

        res += [
            {
                "type": "sale",
                "name": _("Retail Invoices"),
                "code": "RETINV",
                "company_id": company.id,
                "show_on_dashboard": True,
            },
            {
                "type": "sale",
                "name": _("Export Invoices"),
                "code": "EXPINV",
                "company_id": company.id,
                "show_on_dashboard": True,
            },
        ]
        return res
