from odoo import models, fields, api


class SchoolClassroom(models.Model):
    _name = 'school.classroom'
    _description = 'Classroom'
    _order = 'name asc'

    name = fields.Char(string='Class Name', required=True)  # e.g. "Grade 5 - A"
    grade_level = fields.Selection([
        ('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3'),
        ('4', 'Grade 4'), ('5', 'Grade 5'), ('6', 'Grade 6'),
        ('7', 'Grade 7'), ('8', 'Grade 8'), ('9', 'Grade 9'),
        ('10', 'Grade 10'), ('11', 'Grade 11'), ('12', 'Grade 12'),
    ], string='Grade Level', required=True)
    academic_year = fields.Char(string='Academic Year', required=True)  # e.g. "2024-2025"
    teacher_id = fields.Many2one('school.teacher', string='Class Teacher')
    capacity = fields.Integer(string='Capacity', default=30)
    room_number = fields.Char(string='Room Number')

    student_ids = fields.One2many('school.student', 'classroom_id', string='Students')
    subject_ids = fields.Many2many('school.subject', string='Subjects')

    total_students = fields.Integer(string='Total Students', compute='_compute_total_students', store=True)
    available_seats = fields.Integer(string='Available Seats', compute='_compute_total_students', store=True)

    @api.depends('student_ids')
    def _compute_total_students(self):
        for rec in self:
            rec.total_students = len(rec.student_ids)
            rec.available_seats = rec.capacity - rec.total_students


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _order = 'name asc'

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Subject Code', required=True)
    description = fields.Text(string='Description')
    max_grade = fields.Float(string='Max Grade', default=100.0)
    pass_grade = fields.Float(string='Pass Grade', default=50.0)
    teacher_ids = fields.Many2many('school.teacher', string='Teachers')
    classroom_ids = fields.Many2many('school.classroom', string='Classes')
