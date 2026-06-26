from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Full Name', required=True, tracking=True)
    teacher_code = fields.Char(string='Teacher ID', readonly=True, copy=False, default='New')
    image = fields.Binary(string='Photo')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    national_id = fields.Char(string='National ID')
    date_of_birth = fields.Date(string='Date of Birth')
    hire_date = fields.Date(string='Hire Date', default=fields.Date.today)
    salary = fields.Float(string='Salary')
    specialization = fields.Char(string='Specialization')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('resigned', 'Resigned'),
    ], default='active', tracking=True)

    subject_ids = fields.Many2many('school.subject', string='Subjects Taught')
    classroom_ids = fields.One2many('school.classroom', 'teacher_id', string='Classes')
    exam_ids = fields.One2many('school.exam', 'teacher_id', string='Exams')

    total_students = fields.Integer(string='Total Students', compute='_compute_total_students')

    @api.model
    def create(self, vals):
        if vals.get('teacher_code', 'New') == 'New':
            vals['teacher_code'] = self.env['ir.sequence'].next_by_code('school.teacher') or 'New'
        return super().create(vals)

    @api.depends('classroom_ids', 'classroom_ids.student_ids')
    def _compute_total_students(self):
        for rec in self:
            rec.total_students = sum(len(cls.student_ids) for cls in rec.classroom_ids)
