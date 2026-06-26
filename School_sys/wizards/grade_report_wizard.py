from odoo import models, fields, api
from odoo.exceptions import UserError


class GradeReportWizard(models.TransientModel):
    """Wizard to filter and generate grade reports"""
    _name = 'school.grade.report.wizard'
    _description = 'Grade Report Wizard'

    classroom_id = fields.Many2one('school.classroom', string='Class')
    subject_id = fields.Many2one('school.subject', string='Subject')
    exam_type = fields.Selection([
        ('quiz', 'Quiz'), ('midterm', 'Midterm'),
        ('final', 'Final Exam'), ('assignment', 'Assignment'),
    ], string='Exam Type')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_print_report(self):
        domain = []
        if self.classroom_id:
            domain.append(('classroom_id', '=', self.classroom_id.id))
        if self.subject_id:
            domain.append(('subject_id', '=', self.subject_id.id))
        if self.exam_type:
            domain.append(('exam_type', '=', self.exam_type))
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))

        exams = self.env['school.exam'].search(domain)
        if not exams:
            raise UserError("No exams found matching the selected criteria.")

        return self.env.ref('school_system.action_report_grade').report_action(exams)

    def action_view_results(self):
        domain = []
        if self.classroom_id:
            domain.append(('classroom_id', '=', self.classroom_id.id))
        if self.subject_id:
            domain.append(('subject_id', '=', self.subject_id.id))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Exam Results',
            'res_model': 'school.exam.result',
            'view_mode': 'tree',
            'domain': domain,
        }
