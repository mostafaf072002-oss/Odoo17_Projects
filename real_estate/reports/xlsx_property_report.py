from odoo import http
from odoo.http import request

from io import BytesIO
import xlsxwriter
import pandas as pd


class XlsxPropertyReport(http.Controller):

    @http.route(
        "/GET/properties/excel",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False
    )
    def property_excel_report(self, **kwargs):

        properties = request.env["real.estate.property"].sudo().search([])

        output = BytesIO()

        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Properties")

        # Header Format
        header_format = workbook.add_format({
            "bold": True,
            "align": "center",
            "padding": "10px",
        })

        # Headers
        worksheet.write(0, 0, "Name", header_format)
        worksheet.write(0, 1, "Expected Price", header_format)
        worksheet.write(0, 2, "Selling Price", header_format)
        worksheet.write(0, 3, "State", header_format)

        row = 1

        for property in properties:
            worksheet.write(row, 0, property.name or "")
            worksheet.write(row, 1, property.expected_price or 0)
            worksheet.write(row, 2, property.selling_price or 0)
            worksheet.write(row, 3, property.state or "")

            row += 1

        workbook.close()

        output.seek(0)

        return request.make_response(
            output.getvalue(),
            headers=[
                (
                    "Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
                (
                    "Content-Disposition", "attachment; filename=properties.xlsx"
                ),
            ],
        )