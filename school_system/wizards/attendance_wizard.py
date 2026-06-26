from odoo import models, fields, api
from odoo.exceptions import UserError


class AttendanceWizard(models.TransientModel):
    """Bulk attendance marking wizard for a full class"""
    _name = 'school.attendance.wizard'
    _description = 'Mark Class Attendance Wizard'

    classroom_id = fields.Many2one('school.classroom', string='Class', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    default_state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
    ], string='Default Status', default='present', required=True)

    line_ids = fields.One2many('school.attendance.wizard.line', 'wizard_id', string='Students')

    @api.onchange('classroom_id', 'default_state')
    def _onchange_classroom(self):
        if self.classroom_id:
            lines = []
            for student in self.classroom_id.student_ids.filtered(lambda s: s.state == 'active'):
                lines.append((0, 0, {
                    'student_id': student.id,
                    'state': self.default_state,
                }))
            self.line_ids = lines

    def action_confirm(self):
        if not self.line_ids:
            raise UserError("No students to mark attendance for!")

        Attendance = self.env['school.attendance']
        created = 0
        skipped = 0

        for line in self.line_ids:
            existing = Attendance.search([
                ('student_id', '=', line.student_id.id),
                ('date', '=', self.date)
            ])
            if existing:
                skipped += 1
                continue
            Attendance.create({
                'student_id': line.student_id.id,
                'date': self.date,
                'state': line.state,
                'marked_by': self.env.user.id,
            })
            created += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f'Attendance marked: {created} students. Skipped (already exists): {skipped}.',
                'type': 'success',
                'sticky': False,
            }
        }


class AttendanceWizardLine(models.TransientModel):
    _name = 'school.attendance.wizard.line'
    _description = 'Attendance Wizard Line'

    wizard_id = fields.Many2one('school.attendance.wizard', ondelete='cascade')
    student_id = fields.Many2one('school.student', string='Student', required=True)
    state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ], string='Status', required=True, default='present')
    note = fields.Char(string='Note')
