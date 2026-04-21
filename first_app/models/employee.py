import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Staff(models.Model):
    _name = "staff.staff"
    _description = "Staff Table"
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Name",
        required=True,
        index=True
    )

    email = fields.Char(
        string="Email",
        required=True,
        index=True,
        tracking=True
    )

    phone = fields.Char(
        string="Phone",
        required=True,
        tracking=True
    )

    address = fields.Char(string="Address")

    salary = fields.Float(
        string="Salary",
        required=True,
        tracking=True
    )

    type = fields.Char(
        compute="_compute_type",
        string="Type"
    )

    number_of_children = fields.Integer(
        string="Number of Children",
        default=0
    )

    city = fields.Selection(
        [
            ("cairo", "Cairo"),
            ("alex", "Alexandria"),
            ("bani_suef", "Bani Suef"),
        ],
        string="City",
        default="cairo"
    )

    manager = fields.Boolean(
        string="Manager"
    )

    promotion_date = fields.Date()

    project_ids = fields.One2many('project.project', 'staff_id', string="Projects")

    active = fields.Boolean(default=True)

    image = fields.Image(
        string="Image",
    )

    # ✅ SQL Constraints
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'The email address must be unique!'.title()),
        ('check_salary', 'CHECK(salary > 0)','Salary must be greater than zero.')
    ]

    # ✅ Salary Validation
    @api.constrains("salary")
    def _check_salary(self):
        for rec in self:
            if rec.salary <= 0:
                raise ValidationError(_("Salary must be greater than zero."))

    @api.depends('salary')
    def _compute_type(self):
        for rec in self:
            if rec.salary > 10000:
                rec.type = "High Salary"
            else:
                rec.type = "Low Salary"

    @api.onchange('phone')
    def onchange_phone(self):
        for rec in self:
            print(rec.phone)

    def change_city(self):
        selection = self._fields['city'].selection
        cities = [city[0] for city in selection]
        next_city = cities[0]
        for rec in self:
            if cities.index(rec.city) + 1 < len(cities) :
                next_city = cities[cities.index(rec.city) + 1]

            rec.city = next_city

    def show_managers(self):
        return self.env.ref("first_app.manager_action").read()[0]

    def auto_make_manager(self):
        employees = self.env['staff.staff'].search([('salary','>',10000),('manager','=',False)])
        employees.write({
            'manager': True,
            'promotion_date': datetime.date.today()
        })

    def send_email(self):
        for rec in self:
            if rec.email:
                mail = self.env['mail.mail'].create({
                    'subject': 'Promotion',
                    'email_to': rec.email,
                    'body_html': '<p>Congratulations 🎉</p>',
                    })
                mail.send()
                print("Email has been sent.")