odoo.define('plumping_store.ListView', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var rpc = require('web.rpc');
    var core = require('web.core');

    var ListView = AbstractAction.extend({

        template: 'plumping_store.listView',

        init: function (parent, action) {
            this._super(parent, action);

            this.records = [];
            this.results = [];
            this.intervalId = null;
        },

        start: async function () {

            await this.loadRecords();
            await this.report();

            this.intervalId = setInterval(async () => {
                await this.loadRecords();
            }, 3000);

            return this._super.apply(this, arguments);
        },

        destroy: function () {

            if (this.intervalId) {
                clearInterval(this.intervalId);
            }

            this._super.apply(this, arguments);
        },

        /* ==================================
           Load Products
        ================================== */

        loadRecords: async function () {

            try {

                const result = await rpc.query({
                    model: "product.product",
                    method: "search_read",
                    args: [
                        [],
                        ["name"]
                    ],
                });

                this.records = result;

                this.renderElement();

                return this.records;

            } catch (error) {

                console.error(error);

            }
        },

        /* ==================================
           Create Product
        ================================== */

        createRecord: async function () {

            try {

                const record = await rpc.query({
                    model: "product.product",
                    method: "create",
                    args: [{
                        name: "Product30",
                    }],
                });

                await this.loadRecords();

                return record;

            } catch (error) {

                console.error(error);

            }
        },

        /* ==================================
           Sales Report
        ================================== */

        report: async function () {

            try {

                const lines = await rpc.query({
                    model: "sale.order.line",
                    method: "search_read",
                    args: [
                        [
                            ['order_id.state', 'in', ['sale', 'done']]
                        ],
                        [
                            'product_id',
                            'price_subtotal',
                            'product_uom_qty'
                        ]
                    ]
                });

                const productIds = [
                    ...new Set(
                        lines
                            .filter(l => l.product_id)
                            .map(l => l.product_id[0])
                    )
                ];

                if (!productIds.length) {
                    this.results = [];
                    return;
                }

                const products = await rpc.query({
                    model: "product.product",
                    method: "search_read",
                    args: [
                        [
                            ['id', 'in', productIds]
                        ],
                        [
                            'name',
                            'standard_price'
                        ]
                    ]
                });

                const productMap = {};

                products.forEach(function (p) {
                    productMap[p.id] = p;
                });

                const report_dict = {};

                lines.forEach(function (line) {

                    if (!line.product_id) {
                        return;
                    }

                    const productId = line.product_id[0];
                    const productName = line.product_id[1];

                    const productData =
                        productMap[productId] || {};

                    if (!report_dict[productId]) {

                        report_dict[productId] = {
                            product_name: productName,
                            sales_count: 0,
                            total_sales: 0,
                            total_profit: 0,
                        };
                    }

                    report_dict[productId].sales_count += 1;

                    report_dict[productId].total_sales +=
                        line.price_subtotal;

                    const cost =
                        (productData.standard_price || 0) *
                        line.product_uom_qty;

                    const profit =
                        line.price_subtotal - cost;

                    report_dict[productId].total_profit +=
                        profit;
                });

                this.results =
                    Object.values(report_dict);

                console.log(this.results);

                this.renderElement();

                return this.results;

            } catch (error) {

                console.error(error);

            }
        },

    });

    core.action_registry.add(
        'plumping_store.action_list_view',
        ListView
    );

    return ListView;

});