from odoo import http
from odoo.http import request
import json

class PropertyApi(http.Controller):

    @http.route("/GET/properties", type="http", auth="public", methods=['GET'], csrf=False)
    def get_properties(self):
        properties = request.env['real.estate.property'].sudo().search([])

        data = []
        for property in properties:
            data.append({
                'name': property.name,
                'code': property.code,
                'selling_price': property.selling_price,
                'bedrooms': property.bedrooms,
                'bathrooms': property.bathrooms,
                'area': property.area,
                'state': property.state,
                'active': property.active,
            })

        return request.make_json_response(
            {
                'status': 'Success',
                'count': len(data),
                "data": data
            }
        )

    @http.route("/GET/property/<int:property_id>", type="http", auth="public", methods=['GET'], csrf=False)
    def get_property(self, property_id):
        property = request.env['real.estate.property'].sudo().browse(property_id)
        data = [
            {
                'name': property.name,
                'code': property.code,
                'selling_price': property.selling_price,
                'bedrooms': property.bedrooms,
                'bathrooms': property.bathrooms,
                'area': property.area,
                'state': property.state,
                'active': property.active,
            }
        ]

        return request.make_json_response(
            {
                'status': 'Success',
                "data": data
            }
        )

    @http.route("/Post/property", type="http", auth="public", methods=['POST'], csrf=False)
    def create_properties(self, **kwargs):
        args = request.httprequest.data.decode('utf-8')
        vals = json.loads(args)

        property = request.env['real.estate.property'].sudo().create({
            'name': vals.get('name'),
            'selling_price': vals.get('selling_price'),
            'date_available': vals.get('date_available'),
            'bedrooms': vals.get('bedrooms'),
            'bathrooms': vals.get('bathrooms'),
            'area': vals.get('area'),
        })

        return request.make_json_response(
            {
                'status': 'Created Success',
                "name": vals.get('name'),
            }
        )