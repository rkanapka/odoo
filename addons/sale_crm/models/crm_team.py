# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    def _compute_dashboard_button_name(self):
        super()._compute_dashboard_button_name()
        self.filtered(lambda team: team.use_opportunities and team.team_type in ("sales", "website")).update(
            {"dashboard_button_name": _("Pipeline")}
        )
