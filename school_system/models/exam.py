from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolExam(models.Model):
    _name = 'school.exam'
    _description = 'Exam'
    _inherit = ['mail.thread']
    _order = 'date desc'

    name = fields.Char(string='Exam Name', required=True)
    exam_type = fields.Selection([
        ('quiz', 'Quiz'),
        ('midterm', 'Midterm'),
        ('final', 'Final Exam'),
        ('assignment', 'Assignment'),
    ], string='Type', required=True)
    subject_id = fields.Many2one('school.subject', string='Subject', required=True)
    classroom_id = fields.Many2one('school.classroom', string='Class', required=True)
    teacher_id = fields.Many2one('school.teacher', string='Examiner')
    date = fields.Date(string='Exam Date', required=True)
    max_grade = fields.Float(string='Max Grade', required=True, default=100.0)
    pass_grade = fields.Float(string='Pass Grade', default=50.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)

    result_ids = fields.One2many('school.exam.result', 'exam_id', string='Results')
    total_students = fields.Integer(string='Total Students', compute='_compute_stats')
    pass_count = fields.Integer(string='Passed', compute='_compute_stats')
    fail_count = fields.Integer(string='Failed', compute='_compute_stats')
    average_grade = fields.Float(string='Average Grade', compute='_compute_stats')

    @api.depends('result_ids', 'result_ids.grade')
    def _compute_stats(self):
        for rec in self:
            results = rec.result_ids
            rec.total_students = len(results)
            rec.pass_count = len(results.filtered(lambda r: r.grade >= rec.pass_grade))
            rec.fail_count = rec.total_students - rec.pass_count
            rec.average_grade = sum(results.mapped('grade')) / rec.total_students if rec.total_students else 0.0

    def action_confirm(self):
        # Auto-create result records for all students in the class
        for student in self.classroom_id.student_ids:
            existing = self.env['school.exam.result'].search([
                ('exam_id', '=', self.id),
                ('student_id', '=', student.id)
            ])
            if not existing:
                self.env['school.exam.result'].create({
                    'exam_id': self.id,
                    'student_id': student.id,
                    'grade': 0.0,
                })
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_reset_draft(self):
        self.state = 'draft'


class SchoolExamResult(models.Model):
    _name = 'school.exam.result'
    _description = 'Exam Result'
    _order = 'grade desc'

    exam_id = fields.Many2one('school.exam', string='Exam', required=True, ondelete='cascade')
    student_id = fields.Many2one('school.student', string='Student', required=True)
    subject_id = fields.Many2one('school.subject', related='exam_id.subject_id', store=True)
    classroom_id = fields.Many2one('school.classroom', related='exam_id.classroom_id', store=True)
    grade = fields.Float(string='Grade', default=0.0)
    max_grade = fields.Float(related='exam_id.max_grade')
    pass_grade = fields.Float(related='exam_id.pass_grade')
    percentage = fields.Float(string='Percentage (%)', compute='_compute_percentage', store=True)
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ], string='Result', compute='_compute_result', store=True)
    note = fields.Text(string='Notes')

    @api.depends('grade', 'max_grade')
    def _compute_percentage(self):
        for rec in self:
            rec.percentage = (rec.grade / rec.max_grade * 100) if rec.max_grade else 0.0

    @api.depends('grade', 'pass_grade')
    def _compute_result(self):
        for rec in self:
            rec.result = 'pass' if rec.grade >= rec.pass_grade else 'fail'

    @api.constrains('grade', 'max_grade')
    def _check_grade(self):
        for rec in self:
            if rec.grade < 0:
                raise ValidationError("Grade cannot be negative!")
            if rec.grade > rec.max_grade:
                raise ValidationError(f"Grade cannot exceed max grade ({rec.max_grade})!")
