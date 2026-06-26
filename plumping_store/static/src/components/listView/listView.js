/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListView extends Component {
    static template = "plumping_store.listView";

    setup() {

         this.state = useState({
                 "records": [],
                 "results":[],
             });

         this.orm = useService("orm");

         this.rpc = useService("rpc");

         this.loadRecords();

         this.intervalId = setInterval(
         () => { this.loadRecords() },3000
         )

         onWillUnmount(
         () => { clearInterval(this.intervalId) }
         );

         this.report();
    };

    // async loadRecords() {
    //     const result = await this.orm.searchRead("product.product",[],[])
    //     this.state.records = result;
    //     console.log(result);
    //     return this.state.records;
    // };

    async loadRecords() {

            const result = await this.rpc("/web/dataset/call_kw",{
                model: "product.product",
                method: "search_read",
                args:[[]],
                kwargs:{fields:["name"]}
            })

            this.state.records = result;

            return this.state.records;
        };

    async createRecord() {
        const record = await this.rpc("/web/dataset/call_kw",{
            model: "product.product",
            method:"create",
            args:[{
                name: "Product30",
            }],
            kwargs:{}
        })
    }

    async report() {
        // 1️⃣ هات كل sale lines مرة واحدة
        const lines = await this.orm.searchRead(
            "sale.order.line",
            [['order_id.state', 'in', ['sale', 'done']]],
            ['product_id', 'price_subtotal', 'product_uom_qty']
        );

        // 2️⃣ جمع product IDs مرة واحدة
        const productIds = [...new Set(lines.map(l => l.product_id[0]))];

        // 3️⃣ هات المنتجات مرة واحدة
        const products = await this.orm.searchRead(
            "product.product",
            [['id', 'in', productIds]],
            ['name', 'standard_price']
        );

        // 4️⃣ اعمل mapping
        const productMap = {};
        for (let p of products) {
            productMap[p.id] = p;
        }

        const report_dict = {};

        // 5️⃣ loop على lines
        for (let line of lines) {

            const product = line.product_id;
            if (!product) continue;

            const productId = product[0];
            const productName = product[1];

            const productData = productMap[productId];

            if (!report_dict[productId]) {
                report_dict[productId] = {
                    product_name: productName,
                    sales_count: 0,
                    total_sales: 0.0,
                    total_profit: 0.0,
                };
            }

            report_dict[productId].sales_count += 1;
            report_dict[productId].total_sales += line.price_subtotal;

            const cost = (productData?.standard_price || 0) * line.product_uom_qty;
            const profit = line.price_subtotal - cost;

            report_dict[productId].total_profit += profit;
        }

        this.state.results = Object.values(report_dict);

        console.log(this.state.results);

        return this.state.results;
    }
}

registry.category("actions").add("plumping_store.action_list_view", ListView);
console.log("ListView Loaded");