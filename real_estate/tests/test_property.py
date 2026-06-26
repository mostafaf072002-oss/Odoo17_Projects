from odoo.tests.common import TransactionCase
from odoo import fields

class PropertyTest(TransactionCase):

    def setUp(self):
        super(PropertyTest, self).setUp()

        self.first_property = self.env['real.estate.property'].create({
            'name': 'Property_test',
            'selling_price': 100,
            'bedrooms': 2,
        })

    def test_property_created_with_correct_values(self):

        self.assertRecordValues(self.first_property, [{
            'name': 'Property_test',
            'selling_price': 100,
            'bedrooms': 2,
        }])