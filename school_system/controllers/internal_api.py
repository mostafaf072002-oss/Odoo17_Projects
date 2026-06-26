"""
Internal API
============
Endpoints using Odoo's standard JSON-RPC authentication.
Access requires a valid Odoo session (session_id cookie or API key).
Base URL: /api/school/...
"""
import json
from odoo import http
from odoo.http import request


class SchoolInternalAPI(http.Controller):

    # ── Students ────────────────────────────────────────────────

    @http.route('/api/school/students', type='json', auth='user', methods=['GET'])
    def get_students(self, classroom_id=None, state='active', limit=50, offset=0):
        """List students with optional filters"""
        domain = [('state', '=', state)]
        if classroom_id:
            domain.append(('classroom_id', '=', int(classroom_id)))

        students = request.env['school.student'].search(domain, limit=limit, offset=offset)
        total = request.env['school.student'].search_count(domain)

        return {
            'status': 'ok',
            'total': total,
            'data': [{
                'id': s.id,
                'student_code': s.student_code,
                'name': s.name,
                'gender': s.gender,
                'classroom': s.classroom_id.name,
                'attendance_rate': s.attendance_rate,
                'state': s.state,
            } for s in students]
        }

    @http.route('/api/school/students/<int:student_id>', type='json', auth='user', methods=['GET'])
    def get_student(self, student_id):
        """Get single student detail"""
        student = request.env['school.student'].browse(student_id)
        if not student.exists():
            return {'status': 'error', 'message': 'Student not found'}

        return {
            'status': 'ok',
            'data': {
                'id': student.id,
                'student_code': student.student_code,
                'name': student.name,
                'gender': student.gender,
                'age': student.age,
                'classroom': student.classroom_id.name,
                'phone': student.phone,
                'email': student.email,
                'parent_name': student.parent_name,
                'parent_phone': student.parent_phone,
                'attendance_rate': student.attendance_rate,
                'total_fees_due': student.total_fees_due,
                'total_fees_paid': student.total_fees_paid,
                'state': student.state,
            }
        }

    @http.route('/api/school/students', type='json', auth='user', methods=['POST'])
    def create_student(self, **kwargs):
        """Create a new student"""
        required = ['name', 'gender']
        for field in required:
            if field not in kwargs:
                return {'status': 'error', 'message': f'Missing required field: {field}'}

        try:
            student = request.env['school.student'].create(kwargs)
            return {
                'status': 'ok',
                'message': 'Student created successfully',
                'student_id': student.id,
                'student_code': student.student_code,
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # ── Attendance ───────────────────────────────────────────────

    @http.route('/api/school/attendance', type='json', auth='user', methods=['POST'])
    def mark_attendance(self, student_id, date, state, note=None):
        """Mark attendance for a single student"""
        student = request.env['school.student'].browse(int(student_id))
        if not student.exists():
            return {'status': 'error', 'message': 'Student not found'}

        existing = request.env['school.attendance'].search([
            ('student_id', '=', student_id),
            ('date', '=', date)
        ])
        if existing:
            return {'status': 'error', 'message': 'Attendance already marked for this date'}

        att = request.env['school.attendance'].create({
            'student_id': int(student_id),
            'date': date,
            'state': state,
            'note': note,
        })
        return {'status': 'ok', 'attendance_id': att.id}

    # ── Exam Results ─────────────────────────────────────────────

    @http.route('/api/school/exams/<int:exam_id>/results', type='json', auth='user', methods=['GET'])
    def get_exam_results(self, exam_id):
        """Get all results for an exam"""
        exam = request.env['school.exam'].browse(exam_id)
        if not exam.exists():
            return {'status': 'error', 'message': 'Exam not found'}

        return {
            'status': 'ok',
            'exam': exam.name,
            'subject': exam.subject_id.name,
            'average': exam.average_grade,
            'pass_rate': (exam.pass_count / exam.total_students * 100) if exam.total_students else 0,
            'results': [{
                'student': r.student_id.name,
                'student_code': r.student_id.student_code,
                'grade': r.grade,
                'percentage': r.percentage,
                'result': r.result,
            } for r in exam.result_ids]
        }

    # ── Dashboard Stats ──────────────────────────────────────────

    @http.route('/api/school/dashboard', type='json', auth='user', methods=['GET'])
    def get_dashboard_stats(self):
        """Returns summary stats for dashboard"""
        Student = request.env['school.student']
        Teacher = request.env['school.teacher']
        Exam = request.env['school.exam']
        Fee = request.env['school.fee']

        return {
            'status': 'ok',
            'stats': {
                'total_students': Student.search_count([('state', '=', 'active')]),
                'total_teachers': Teacher.search_count([('state', '=', 'active')]),
                'total_exams_this_month': Exam.search_count([]),
                'fees_collected': sum(Fee.search([('state', '=', 'paid')]).mapped('amount')),
                'fees_overdue': sum(Fee.search([('state', '=', 'overdue')]).mapped('amount')),
                'students_by_gender': {
                    'male': Student.search_count([('gender', '=', 'male'), ('state', '=', 'active')]),
                    'female': Student.search_count([('gender', '=', 'female'), ('state', '=', 'active')]),
                }
            }
        }
