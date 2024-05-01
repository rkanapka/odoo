# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, models


class WebsitePlanner(models.Model):
    _inherit = "web.planner"

    @api.model
    def _get_planner_application(self):
        planner = super()._get_planner_application()
        planner.append(["planner_website", "Website Planner"])
        return planner

    @api.model
    def _prepare_planner_website_data(self):
        values = {
            "company_id": self.env.user.company_id,
        }
        return values
