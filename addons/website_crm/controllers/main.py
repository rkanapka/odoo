# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.website_form.controllers.main import WebsiteForm

from odoo import http
from odoo.http import request


class WebsiteForm(WebsiteForm):

    # Check and insert values from the form on the model <model>
    @http.route("/website_form/<string:model_name>", type="http", auth="public", methods=["POST"], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == "crm.lead" and not request.params.get("state_id"):
            geoip_country_code = request.session.get("geoip", {}).get("country_code")
            geoip_state_code = request.session.get("geoip", {}).get("region")
            if geoip_country_code and geoip_state_code:
                State = request.env["res.country.state"]
                request.params["state_id"] = State.search(
                    [("code", "=", geoip_state_code), ("country_id.code", "=", geoip_country_code)]
                ).id

        return super().website_form(model_name, **kwargs)
