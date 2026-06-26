from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolAttendance(models.Model):
    _name = 'school.attendance'
    _description = 'Student Attendance'
    _order = 'date desc'

    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    classroom_id = fields.Many2one('school.classroom', string='Class',
                                   related='student_id.classroom_id', store=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ], string='Status', required=True, default='present')
    note = fields.Char(string='Note')
    marked_by = fields.Many2one('res.users', string='Marked By', default=lambda self: self.env.user)

    _sql_constraints = [
        ('unique_student_date', 'UNIQUE(student_id, date)',
         'Attendance for this student on this date already exists!')
    ]

    @api.constrains('date')
    def _check_date(self):
        for rec in self:
            if rec.date > fields.Date.today():
                raise ValidationError("Cannot mark attendance for a future date!")
