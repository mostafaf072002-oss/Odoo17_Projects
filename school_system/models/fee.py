from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolFee(models.Model):
    _name = 'school.fee'
    _description = 'Student Fee'
    _inherit = ['mail.thread']
    _order = 'due_date asc'

    name = fields.Char(string='Fee Reference', readonly=True, copy=False, default='New')
    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    classroom_id = fields.Many2one('school.classroom', related='student_id.classroom_id', store=True)
    fee_type = fields.Selection([
        ('tuition', 'Tuition Fee'),
        ('transport', 'Transport Fee'),
        ('activity', 'Activity Fee'),
        ('exam', 'Exam Fee'),
        ('other', 'Other'),
    ], string='Fee Type', required=True)
    amount = fields.Float(string='Amount', required=True)
    due_date = fields.Date(string='Due Date', required=True)
    payment_date = fields.Date(string='Payment Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)
    note = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('school.fee') or 'New'
        return super().create(vals)

    def action_confirm(self):
        self.state = 'due'

    def action_pay(self):
        self.state = 'paid'
        self.payment_date = fields.Date.today()

    def action_cancel(self):
        self.state = 'cancelled'

    def action_check_overdue(self):
        """Called by cron to mark overdue fees"""
        today = fields.Date.today()
        overdue = self.search([
            ('state', '=', 'due'),
            ('due_date', '<', today)
        ])
        overdue.write({'state': 'overdue'})
