from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'
    price = fields.Float(string='Price', related="staff_id.salary")
    staff_id = fields.Many2one('staff.staff',string='Staff')

    # @api.depends('staff_id')
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price = rec.staff_id.salary