from odoo import models, fields, api

class QuickSaleOrderWizard(models.TransientModel):
    _name = 'quick.sale.order.wizard'
    _description = 'Quick Sale Order Wizard'

    partner_id = fields.Many2one('res.partner', required=True)
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Integer('Quantity', default=1)

    def create_order(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
        })

        order_line = self.env['sale.order.line'].create({
            "order_id": order.id,
            "product_id": self.product_id.id,
            "product_uom_qty": self.quantity,
        })
