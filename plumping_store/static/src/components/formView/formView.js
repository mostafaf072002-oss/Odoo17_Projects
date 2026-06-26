/* @odoo-module */

import { Component, useState, onWillUnmount, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class FormView extends Component {
    static template = "plumping_store.formView";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");

        this.state = useState({
            name: "",
            products:[],
            loading: false,
        });

        onWillStart(async () => {
            await this.loadProducts();
        });
    }

    // تحميل البيانات
    async loadProducts() {
        this.state.products = await this.orm.searchRead(
            "product.product",
            [],
            ["name"]
        );
    }

    async createProduct() {
        if (!this.state.name) {
            this.notification.add("Name is required", {type: "Warning"});
            return;
        }

        try {
            this.state.loading = true;

            const id = await this.orm.create("product.product", [{
                name: this.state.name,
            }]);

            this.notification.add("Product created", {type: "Success"});

            this.state.name = "";

            await this.loadProducts();

        } catch (error) {
            this.notification.add("Can't Create Product", {type: "danger"});
            cosole.log(error);
        } finally {
            this.state.loading = false;
        }
    }

    // حذف منتج
    async deleteRecord(id) {
        await this.orm.unlink("product.product", [id]);
        await this.loadProducts();
    }

}

registry.category("actions").add("plumping_store.form_view", FormView);
console.log("Form View Loaded");