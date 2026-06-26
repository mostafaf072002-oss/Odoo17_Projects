import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ref = fields.Char(string="Reference", readonly=True, copy=False, default="New")
    min_quantity = fields.Integer(string="Minimum Quantity", default=0)
    is_low_stock = fields.Boolean(
        string="Is Low Stock",
        compute="_compute_is_low_stock",
        store=True
    )
    is_plumbing = fields.Boolean(string="Is Plumbing")
    brand = fields.Char(string="Brand")
    material = fields.Selection([
        ('pvc', 'PVC'),
        ('copper', 'Copper'),
        ('steel', 'Steel'),
    ], string="Material")
    diameter = fields.Float(string="Diameter")
    margin = fields.Float(string="Margin", compute="_compute_margin")

    @api.depends('qty_available', 'min_quantity')
    def _compute_is_low_stock(self):
        for rec in self:
            rec.is_low_stock = rec.qty_available < rec.min_quantity

    @api.depends('list_price', 'standard_price', 'taxes_id')
    def _compute_margin(self):
        for rec in self:
            # Proper way to calculate price with taxes in Odoo
            taxes = rec.taxes_id.compute_all(rec.list_price, product=rec, partner=self.env.user.partner_id)
            price_with_tax = taxes['total_included']
            rec.margin = price_with_tax - rec.standard_price

    def check_low_stock(self):
        # We can search now because store=True
        products = self.search([('is_low_stock', '=', True)])
        if not products:
            _logger.info("No low stock products found.")
            return

        product_list = "\n".join([f"- {p.name} (Qty: {p.qty_available})" for p in products])
        _logger.info(f"Products With Low Stock:\n{product_list}")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env["ir.sequence"].next_by_code("product_seq") or "New"
        return super(ProductTemplate, self).create(vals_list)

