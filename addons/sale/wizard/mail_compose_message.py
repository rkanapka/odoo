# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.multi
    def send_mail(self, auto_commit=False):
        if (
            self._context.get("default_model") == "sale.order"
            and self._context.get("default_res_id")
            and self._context.get("mark_so_as_sent")
        ):
            order = self.env["sale.order"].browse([self._context["default_res_id"]])
            if order.state == "draft":
                order.with_context(tracking_disable=True).state = "sent"
            self = self.with_context(mail_post_autofollow=True, lang=order.partner_id.lang)
        return super().send_mail(auto_commit=auto_commit)
