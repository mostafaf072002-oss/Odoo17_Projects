from odoo import http
from odoo.http import request

class ProductController(http.Controller):

    @http.route("/api/products", type="http", methods=["GET"], auth="public", csrf=False)
    def get_products(self, **kwargs):
        products = request.env["product.product"].sudo().search([])

        data = [{
            "id": p.id,
            "name": p.name,
        } for p in products]

        return request.make_json_response({
            "products": data
        })