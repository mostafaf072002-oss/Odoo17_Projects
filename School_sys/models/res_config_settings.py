from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    school_external_api_key = fields.Char(
        string='External API Key',
        config_parameter='school_system.external_api_key'
    )
    school_external_api_url = fields.Char(
        string='External API Base URL',
        config_parameter='school_system.external_api_url'
    )
    school_sms_api_key = fields.Char(
        string='SMS Gateway API Key',
        config_parameter='school_system.sms_api_key'
    )
