from odoo import models, fields

class Project(models.Model):
    _name = 'project.project'
    _description = 'Project'
    name = fields.Char(required=True)

    staff_id = fields.Many2one('staff.staff')
