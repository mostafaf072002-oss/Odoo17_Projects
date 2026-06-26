from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import requests
import json

class Property(models.Model):
    _name = 'real.estate.property'
    _description = 'Real estate property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_available asc'

    img = fields.Image(string='Image', attachment=True)
    code = fields.Char(string='Property Code', copy=False, readonly=True, default='NEW')
    name = fields.Char(string='Property Name', required=True, translate=True, index=True, copy=False, tracking=True)
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    area = fields.Float(string='Area')
    active = fields.Boolean(string='Active', default=True)
    date_available = fields.Datetime(string='Date Available')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft')

    # ========== Constraints ========== #
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name must be unique'),
    ]

    @api.constrains('expected_price')
    def _check_price(self):
        for rec in self:
            if rec.expected_price <= 0:
                raise ValidationError('Price must be greater than 0')

    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError('Bedrooms must be greater than 0')

    @api.model
    def create(self, vals):
        if vals.get('code','NEW') == 'NEW':
            vals['code'] = self.env["ir.sequence"].next_by_code('property_seq') or "NEW"

        return super().create(vals)

    # ================== Button Methods ================== #

    def set_draft(self):
        for rec in self:
            rec.state = 'draft'

    def set_available(self):
        for rec in self:
            rec.state = 'available'

    def set_sold(self):
        for rec in self:
            rec.state = 'sold'

        # url = "http://api.apis.guru/v2/list.json"
        #
        # response = requests.get(
        #     url,
        # )

        # print(response.json())

    def set_cancelled(self):
        for rec in self:
            rec.state = 'cancel'

    # ========= Server Actions ======== #
    def sold_property(self):
        template = self.env.ref( 'real_estate.email_template_property_sold')
        print("Template Opened")

        for rec in self:
            # Change State
            rec.state = 'sold'

            # Chatter Notification
            rec.message_post(
                body="Property sold successfully"
            )

            # Send Email
            if self.env.user.email:
                template.send_mail(
                    rec.id,
                    email_values={
                        'email_to': self.env.user.email
                    },
                    force_send=True
                )

    def property_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/GET/properties/excel',
            'target': 'new'
        }

