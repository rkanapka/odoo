# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    purchase_line_ids = fields.One2many("purchase.order.line", "sale_line_id")

    @api.multi
    def _get_qty_procurement(self):
        # People without purchase rights should be able to do this operation
        purchase_lines_sudo = self.sudo().purchase_line_ids
        if purchase_lines_sudo.filtered(lambda r: r.state != "cancel"):
            qty = 0.0
            for po_line in purchase_lines_sudo.filtered(lambda r: r.state != "cancel"):
                qty += po_line.product_uom._compute_quantity(
                    po_line.product_qty, self.product_uom, rounding_method="HALF-UP"
                )
            return qty
        else:
            return super()._get_qty_procurement()
