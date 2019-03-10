from odoo import fields as old_fields
from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'
<<<<<<< HEAD
    _columns = {
        'name': old_fields.char('Name', required=True, index=True, track_visibility='onchange'),
        'phone': old_fields.char('Phone', track_visibility='onchange'),
    }
=======

    name = old_fields.Char('Name', required=True, index=True, track_visibility='onchange')
    phone = old_fields.Char('Phone', track_visibility='onchange')
>>>>>>> github/11.0
