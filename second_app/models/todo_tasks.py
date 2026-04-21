import datetime

from odoo import models, fields, api, _

class TodoTask(models.Model):
    _name = "todo.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "To-Do Table"
    _rec_name = "name"

    ref = fields.Char(
        default="New",
        string="Reference",
        readonly=True
    )
    name = fields.Char(
        required=True,
        string="Name",
        tracking=True
    )

    assign_to = fields.Many2one(
        "res.partner",
        string="Assign To"
    )
    description = fields.Char(
        string="Description"
    )
    due_date = fields.Date(
        string="Due Date"
    )
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ],
    default="new",
    string="Status",
    tracking=True
    )
    type = fields.Selection(
        [
            ('in_progress', 'In Progress'),
            ('closed', 'Closed')
        ],
       # compute='_compute_due_date',
        string="Type",
        default="in_progress"
    )
    active = fields.Boolean(
        default=True
    )

    image = fields.Image(string="Image")
    def action_completed(self):
        for rec in self:
            rec.status = 'completed'

    @api.model
    def action_check_due_date(self):
        ids = self.search([('status', '!=', 'completed')])
        for rec in ids:
            if rec.due_date and rec.due_date < datetime.date.today():
                rec.type = 'closed'
            else:
                rec.type = 'in_progress'

    @api.depends('due_date')
    def _compute_due_date(self):
        today = datetime.date.today()
        for rec in self:
            if rec.due_date and rec.due_date < today:
                rec.type = 'closed'
            else:
                rec.type = 'in_progress'  # ✅ مهم جدًا

    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)

        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('task_sequence')

        return res

    def check_completed(self):
        for rec in self:
            if rec.status == 'completed':
                print(rec.status)



    def change_status_action(self):
        action = self.env['ir.actions.actions']._for_xml_id('second_app.change_status_wizard_action')
        action['context'] = {
            'default_task_id': self.id,
        }
        return action