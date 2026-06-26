from odoo import http
from odoo.http import request

class ProductController(http.Controller):

    @http.route("/api/products", type="http", methods=["GET"], auth="public", csrf=False)
    def get_products(self):
        products = request.env["product.product"].sudo().search([])

        data = [{
            "id": p.id,
            "name": p.name,
        } for p in products]

        return request.make_json_response({
            "products": data
        })

# from odoo import http
# from odoo.http import request
#
# class ProductAPI(http.Controller):
#
#     @http.route("/product/form", type="http", auth="user", website=True)
#     def product_form(self, **kwargs):
#         return request.render("plumping_store.template_name")
#
#     @http.route("/product/create", type="http", methods=['POST'], auth="user", csrf=False)
#     def create_record(self, **kwargs):
#         name = kwargs.get('name')
#
#         request.env["product.product"].create({"name": name})
#
#         return {f"Product: {name} Is Created"}