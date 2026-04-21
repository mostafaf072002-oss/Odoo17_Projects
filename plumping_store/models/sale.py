from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    plumping_note = fields.Char(string='Plumping Note')

    def get_product_sales(self):

        lines = self.env['sale.order.line'].search([
            ('order_id.state', 'in', ['sale', 'done'])
        ])

        result = {}

        for line in lines:
            product = line.product_id

            if product.id not in result:
                result[product.id] = {
                    'product_name': product.name,
                    'sales_count': 0,
                    'total_sales': 0.0,
                    'total_profit': 0.0,
                }

            result[product.id]['sales_count'] += 1
            result[product.id]['total_sales'] += line.price_subtotal

            cost = product.standard_price * line.product_uom_qty
            profit = line.price_subtotal - cost

            result[product.id]['total_profit'] += profit

            report_data = list(result.values())

        print(report_data)

        return {
            'report_data': report_data,
        }
