from odoo import models, api

class ProductSalesService(models.AbstractModel):
    _name = 'product.sales.service'
    _description = 'Product Sales Service'

    @api.model
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

        return {
            'report_data': list(result.values())
        }