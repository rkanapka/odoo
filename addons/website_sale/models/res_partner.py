# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    last_website_so_id = fields.Many2one("sale.order", string="Last Online Sales Order", copy=False)
