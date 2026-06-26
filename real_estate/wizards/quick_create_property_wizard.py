from odoo import models, fields, api

class PropertyWizard(models.TransientModel):
    _name = 'wizard.real.estate.property'
    _description = 'Property Wizard'

    name = fields.Char(string='Property Name', translate=True, index=True, copy=False)
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    area = fields.Float(string='Area')
    date_available = fields.Datetime(string='Date Available')

    def create_property(self):
        self.env['real.estate.property'].create({
            'name': self.name,
            'selling_price': self.selling_price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area': self.area,
            'date_available': self.date_available,
        })

        return {
            'type': 'ir.actions.act_window_close'
        }