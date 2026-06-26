/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted, useState, xml } from "@odoo/owl";

class SchoolDashboard extends Component {
    static template = xml`
        <div class="school_dashboard o_view_controller">
            <t t-if="state.loading">
                <div class="text-center p-5">
                    <i class="fa fa-spinner fa-spin fa-3x text-primary"/>
                    <p class="mt-2">Loading dashboard...</p>
                </div>
            </t>
            <t t-else="">
                <div class="school_dash_header">
                    <h2><i class="fa fa-graduation-cap me-2"/>School Management Dashboard</h2>
                </div>
                <div class="school_kpi_row">
                    <div class="school_kpi_card students" t-on-click="openStudents">
                        <div class="kpi_icon"><i class="fa fa-users"/></div>
                        <div class="kpi_value"><t t-esc="state.stats.total_students"/></div>
                        <div class="kpi_label">Active Students</div>
                    </div>
                    <div class="school_kpi_card teachers" t-on-click="openTeachers">
                        <div class="kpi_icon"><i class="fa fa-user-tie"/></div>
                        <div class="kpi_value"><t t-esc="state.stats.total_teachers"/></div>
                        <div class="kpi_label">Teachers</div>
                    </div>
                    <div class="school_kpi_card fees" t-on-click="openFees">
                        <div class="kpi_icon"><i class="fa fa-money-bill-wave"/></div>
                        <div class="kpi_value">EGP <t t-esc="state.stats.fees_collected"/></div>
                        <div class="kpi_label">Fees Collected</div>
                    </div>
                    <div class="school_kpi_card overdue" t-on-click="openFees">
                        <div class="kpi_icon"><i class="fa fa-exclamation-triangle"/></div>
                        <div class="kpi_value">EGP <t t-esc="state.stats.fees_overdue"/></div>
                        <div class="kpi_label">Fees Overdue</div>
                    </div>
                </div>
                <div class="school_gender_row mt-4">
                    <div class="school_gender_card">
                        <h5>Students by Gender</h5>
                        <div class="d-flex justify-content-around mt-3">
                            <div class="text-center">
                                <i class="fa fa-male fa-3x text-primary"/>
                                <h4><t t-esc="state.stats.students_by_gender.male"/></h4>
                                <small>Male</small>
                            </div>
                            <div class="text-center">
                                <i class="fa fa-female fa-3x text-danger"/>
                                <h4><t t-esc="state.stats.students_by_gender.female"/></h4>
                                <small>Female</small>
                            </div>
                        </div>
                    </div>
                    <div class="school_quicklinks_card">
                        <h5>Quick Actions</h5>
                        <div class="d-grid gap-2 mt-3">
                            <button class="btn btn-outline-primary" t-on-click="openAttendance">
                                <i class="fa fa-check-square me-2"/>Mark Attendance
                            </button>
                            <button class="btn btn-outline-success" t-on-click="openStudents">
                                <i class="fa fa-user-plus me-2"/>Add Student
                            </button>
                            <button class="btn btn-outline-warning" t-on-click="openFees">
                                <i class="fa fa-file-invoice-dollar me-2"/>View Fees
                            </button>
                        </div>
                    </div>
                </div>
            </t>
        </div>
    `;

    setup() {
        this.rpc = useService("rpc");
        this.actionService = useService("action");
        this.state = useState({
            loading: true,
            stats: {
                total_students: 0,
                total_teachers: 0,
                fees_collected: 0,
                fees_overdue: 0,
                students_by_gender: { male: 0, female: 0 },
            },
        });
        onMounted(() => this._loadStats());
    }

    async _loadStats() {
        try {
            const result = await this.rpc("/api/school/dashboard");
            if (result && result.status === "ok") {
                this.state.stats = result.stats;
            }
        } catch (e) {
            console.error("School dashboard load error:", e);
        } finally {
            this.state.loading = false;
        }
    }

    openStudents()   { this.actionService.doAction("school_system.action_school_student"); }
    openTeachers()   { this.actionService.doAction("school_system.action_school_teacher"); }
    openFees()       { this.actionService.doAction("school_system.action_school_fee"); }
    openAttendance() { this.actionService.doAction("school_system.action_attendance_wizard"); }
}

registry.category("actions").add("school_dashboard", SchoolDashboard);
