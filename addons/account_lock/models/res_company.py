from odoo import api, models



TEST_PRE_COMMIT ={'foo': 123}

class ResCompany(models.Model):
    _inherit = "res.company"

    @api.multi
    def write(self, vals):
        # fiscalyear_lock_date can't be set to a prior date
        if "fiscalyear_lock_date" in vals or "period_lock_date" in vals:
            self._check_lock_dates(vals)
        return super().write(vals)
