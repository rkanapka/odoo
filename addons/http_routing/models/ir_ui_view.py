# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.http_routing.models.ir_http import slug, unslug_url

from odoo import api, models


class IrUiView(models.Model):
    _inherit = ["ir.ui.view"]

    @api.model
    def _prepare_qcontext(self):
        qcontext = super()._prepare_qcontext()
        qcontext["slug"] = slug
        qcontext["unslug_url"] = unslug_url
        return qcontext
