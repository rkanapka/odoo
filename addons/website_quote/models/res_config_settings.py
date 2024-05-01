# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    default_template_id = fields.Many2one("sale.quote.template", default_model="sale.order", string="Default Template")
