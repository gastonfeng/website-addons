from odoo import fields as old_fields
from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = old_fields.Char('Name', required=True, index=True, track_visibility='onchange')
    phone = old_fields.Char('Phone', track_visibility='onchange')
