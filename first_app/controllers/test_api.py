from odoo import http

class testApi(http.Controller):
    @http.route("/test", type="http", auth="none", methods=["GET"], csrf=False)
    def test_endpoint(self):
        print("test_endpoint")