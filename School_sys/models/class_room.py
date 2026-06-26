from odoo import models, fields, api
from odoo.exceptions import ValidationError

class class_room(models.Model):
    _name = 'school.class.room'
    _description = 'Class Room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    #------------- Basic Info -------------
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, tracking=True, default='NEW', copy=False)
