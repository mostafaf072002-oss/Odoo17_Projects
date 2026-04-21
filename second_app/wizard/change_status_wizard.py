from odoo import models, fields

class ChangeStatus(models.TransientModel):
    _name = 'change.status'
    _description = 'Change Status'

    task_id = fields.Many2one('todo.task')
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress')
    ])
    reason = fields.Char('Reason')

    def action_completed(self):
        self.task_id.status = self.status

    def change_status_action(self):
        action = self.env['ir.actions.actions']._for_xml_id('second_app.change_status_wizard_action')
        action['context'] = {
            'default_task_id': self.id,
        }
        return action