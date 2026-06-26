from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    # ──────────────── Basic Info ────────────────
    name = fields.Char(string='Full Name', required=True, tracking=True)
    student_code = fields.Char(string='Student ID', readonly=True, copy=False, default='New')
    image = fields.Binary(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    national_id = fields.Char(string='National ID')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')

    # ── Academic Info ────────────────────────────────────────
    classroom_id = fields.Many2one('school.classroom', string='Class', tracking=True)
    enrollment_date = fields.Date(string='Enrollment Date', default=fields.Date.today)
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('expelled', 'Expelled'),
    ], string='Status', default='active', tracking=True)

    # ── Parent Info ──────────────────────────────────────────
    parent_name = fields.Char(string='Parent Name')
    parent_phone = fields.Char(string='Parent Phone')
    parent_email = fields.Char(string='Parent Email')

    # ── Relational Fields ────────────────────────────────────
    attendance_ids = fields.One2many('school.attendance', 'student_id', string='Attendance')
    exam_result_ids = fields.One2many('school.exam.result', 'student_id', string='Exam Results')
    fee_ids = fields.One2many('school.fee', 'student_id', string='Fees')

    # ── Computed ─────────────────────────────────────────────
    attendance_rate = fields.Float(string='Attendance Rate (%)', compute='_compute_attendance_rate', store=True)
    total_fees_due = fields.Float(string='Total Fees Due', compute='_compute_fees')
    total_fees_paid = fields.Float(string='Total Fees Paid', compute='_compute_fees')

    # ────────────────────────────────────────────────────────
    @api.model
    def create(self, vals):
        if vals.get('student_code', 'New') == 'New':
            vals['student_code'] = self.env['ir.sequence'].next_by_code('school.student') or 'New'
        return super().create(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - (
                    (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day)
                )
            else:
                rec.age = 0

    @api.depends('attendance_ids', 'attendance_ids.state')
    def _compute_attendance_rate(self):
        for rec in self:
            total = len(rec.attendance_ids)
            if total:
                present = len(rec.attendance_ids.filtered(lambda a: a.state == 'present'))
                rec.attendance_rate = (present / total) * 100
            else:
                rec.attendance_rate = 0.0

    @api.depends('fee_ids', 'fee_ids.amount', 'fee_ids.state')
    def _compute_fees(self):
        for rec in self:
            rec.total_fees_due = sum(rec.fee_ids.mapped('amount'))
            rec.total_fees_paid = sum(
                rec.fee_ids.filtered(lambda f: f.state == 'paid').mapped('amount')
            )

    @api.constrains('national_id')
    def _check_national_id(self):
        for rec in self:
            if rec.national_id:
                duplicate = self.search([
                    ('national_id', '=', rec.national_id),
                    ('id', '!=', rec.id)
                ])
                if duplicate:
                    raise ValidationError(f"National ID {rec.national_id} already exists!")

    def action_activate(self):
        self.state = 'active'

    def action_deactivate(self):
        self.state = 'inactive'

    def action_graduate(self):
        self.state = 'graduated'
