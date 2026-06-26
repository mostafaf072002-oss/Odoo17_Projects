/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class Dashboard extends Component {
    // Call Template
    static template = "real_estate.dashboard_template";

    setup() {
        /* =============================
           Services
        ============================= */
        this.orm = useService("orm");

        /* =============================
           Refs
        ============================= */
        this.pieChartRef = useRef("pieChart");
        this.barChartRef = useRef("barChart");

        /* =============================
           Reactive State
        ============================= */
        this.state = useState({
            records: [],
            type: "pie",
            name: "",
            selling_price: "",
            bedrooms: "",
            bathrooms: "",
            area: "",
            date_available: "",
        });

        /* =============================
           Initial Load
        ============================= */
        onMounted(async () => {
            await this.loadProperties();

            await this.renderChart();
        });

        /* =============================
           Auto Refresh
        ============================= */
        this.interval = setInterval(async () => {
            await this.loadProperties();

            /* Destroy old chart */
            if (this.pieChart) { this.pieChart.destroy(); }
            if (this.pieChart) { this.barChart.destroy(); }

            /* Render new chart */
            await this.renderChart();
        }, 10000);

        /* =============================
           Cleanup
        ============================= */
        onWillUnmount(() => {
            clearInterval(this.interval);

            if (this.pieChart) { this.pieChart.destroy(); }
        });
    }

    /* =====================================
       Load Properties
    ===================================== */

    async loadProperties() {

        try {
            const properties =
                await this.orm.searchRead(
                    "real.estate.property",
                    [],
                    [
                        "name",
                        "selling_price",
                        "bedrooms",
                        "bathrooms",
                        "area",
                        "date_available",
                    ]
                );

            this.state.records = properties;
        }

        catch(error) {

            console.error(error);

        }
    }

    /* =====================================
       Create Property
    ===================================== */

    async createProperty() {
        try {

            await this.orm.create(
                "real.estate.property",
                [{
                    name: this.state.name,
                    selling_price: parseFloat(this.state.selling_price),
                    bedrooms: parseInt(this.state.bedrooms),
                    bathrooms: parseInt(this.state.bathrooms),
                    area: parseFloat(this.state.area),
                    date_available: this.state.date_available,
                }]
            );

            /* Reload data */
            await this.loadProperties();

            /* Refresh chart */
            if (this.pieChart) {
                this.pieChart.destroy();
            }
            if (this.barChart) {
                this.barChart.destroy();
            }

            await this.renderChart();

            /* Clear form */
            this.cancel();

        }

        catch(error) {
            console.error(error);
        }
    }

    /* =====================================
       Reset Form
    ===================================== */
    cancel() {
        this.state.name = "";
        this.state.selling_price = "";
        this.state.bedrooms = "";
        this.state.bathrooms = "";
        this.state.area = "";
        this.state.date_available = "";
    }

    /* =====================================
       Render Chart
    ===================================== */
    async renderChart() {
        try {
            const properties =
                await this.orm.searchRead(
                    "real.estate.property",
                    [],
                    [
                        "name",
                        "selling_price"
                    ]
                );

            /* =============================
               Labels
            ============================= */
            const labels = properties.map(
                property => property.name
            );

            /* =============================
               Prices
            ============================= */
            const prices = properties.map(
                property => property.selling_price
            );

            /* =============================
               Chart Data
            ============================= */
            const data = {
                labels: labels,

                datasets: [{
                    label: "Selling Price",
                    data: prices,
                    borderWidth: 1,
                }]
            };

            /* =============================
               Chart Config
            ============================= */
            const pieConfig = {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            };
            const barConfig = {
                            type: 'bar',
                            data: data,
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }
                        };

            /* =============================
               Canvas
            ============================= */
            const pieCanvas = this.pieChartRef.el;
            const barCanvas = this.barChartRef.el;

            /* =============================
               Create Chart
            ============================= */
            this.pieChart = new Chart(
                pieCanvas,
                pieConfig
            );
            this.barChart = new Chart(
                barCanvas,
                barConfig
            );

        }
        catch(error) {
            console.error(error);
        }
    }

}



/* =====================================
   Register Action
===================================== */
registry.category("actions").add( "real_estate_dashboard", Dashboard );