# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Extension0(models.Model):
    _name = "extension.0"

    name = fields.Char(default="A")


class Extension1(models.Model):
    _inherit = "extension.0"

    description = fields.Char(default="Extended")
