import json
from odoo import http
from odoo.http import request
from urllib.parse import parse_qs

class staff_api(http.Controller):
    @http.route("/v1/staff", type="http", auth="none", methods=["POST"], csrf=False)
    def create_staff(self):
        args = request.httprequest.data.decode("utf-8")
        vals =json.loads(args)
        try:
            staff = request.env["staff.staff"].sudo().create(vals)
            if staff:
                # return vals
                return request.make_json_response({
                    "message": "Staff created successfully",
                    "id": staff.id,
                    "name": staff.name,
                }, status=200)
        except Exception as e:
            return request.make_json_response({
                "message": e,
            }, status=400)

    @http.route("/v1/staff/<int:staff_id>", type="http", auth="none", methods=["POST", "PUT"], csrf=False)
    def update_staff(self, staff_id, **kwargs):
        # Search for the record
        staff = request.env["staff.staff"].sudo().browse(staff_id)

        if not staff.exists():
            return request.make_json_response({"error": "Not Found"}, status=404)

        # Receive Data From User
        args = request.httprequest.data.decode("utf-8")
        vals = json.loads(args)
        staff.update(vals)

        return request.make_json_response({
            "message": f"Staff {staff_id} updated successfully",
        }, status=200)

    @http.route("/v1/staff/<int:staff_id>", type="http", auth="none", methods=["GET"], csrf=False)
    def show_staff(self, staff_id, **kwargs):
        # Search for the record
        staff = request.env["staff.staff"].sudo().browse(staff_id)

        if not staff.exists():
            return request.make_json_response({"error": "Not Found"}, status=404)


        return request.make_json_response({
            "message": f"Staff {staff_id} updated successfully",
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
        }, status=200)

    @http.route("/v1/staff", type="http", auth="none", methods=["GET"], csrf=False)
    def show_staffs(self):
        # Search for the records
        params = parse_qs(request.httprequest.query_string.decode("utf-8"))
        staffs = request.env["staff.staff"].sudo().search([("type","=",params.get("type"))])

        if not staffs:
            return request.make_json_response({"error": "Not Found"}, status=404)

        return request.make_json_response([{
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
        } for staff in staffs], status=200)
