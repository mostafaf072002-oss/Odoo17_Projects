from odoo import models, fields

class PlumbingDashboard(models.TransientModel):
    _name = "plumbing.dashboard"
    _description = "Plumbing Dashboard"

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user
    )

