"""
External API
============
1. Public Webhook endpoints (receive data FROM external systems)
2. Outbound API calls (push/pull data TO external systems)
   - SMS Gateway (notify parents)
   - External Student Database sync
"""
import json
import logging
import requests
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# PART 1 — INBOUND: Receive data from external systems (Webhooks)
# ═══════════════════════════════════════════════════════════════

class SchoolWebhookController(http.Controller):

    def _verify_token(self, token):
        """Simple token validation against stored API key"""
        stored = request.env['ir.config_parameter'].sudo().get_param(
            'school_system.external_api_key'
        )
        return token and stored and token == stored

    @http.route('/webhook/school/student/sync', type='json', auth='none',
                methods=['POST'], csrf=False)
    def webhook_student_sync(self, **kwargs):
        """
        Receive student data from an external system.
        Expected payload:
        {
          "token": "...",
          "students": [
            {"national_id": "...", "name": "...", "gender": "male", "phone": "..."},
            ...
          ]
        }
        """
        try:
            payload = json.loads(request.httprequest.data)

            if not self._verify_token(payload.get('token')):
                return {'status': 'error', 'message': 'Unauthorized'}

            Student = request.env['school.student'].sudo()
            created, updated = 0, 0

            for data in payload.get('students', []):
                national_id = data.get('national_id')
                existing = Student.search([('national_id', '=', national_id)], limit=1)

                if existing:
                    existing.write({k: v for k, v in data.items() if k != 'national_id'})
                    updated += 1
                else:
                    Student.create(data)
                    created += 1

            _logger.info(f"Webhook student sync: {created} created, {updated} updated")
            return {'status': 'ok', 'created': created, 'updated': updated}

        except Exception as e:
            _logger.error(f"Webhook error: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    @http.route('/webhook/school/fee/payment', type='json', auth='none',
                methods=['POST'], csrf=False)
    def webhook_fee_payment(self, **kwargs):
        """
        Receive payment confirmation from external payment gateway.
        Payload: {"token": "...", "fee_ref": "FEE/2024/0001", "status": "paid"}
        """
        try:
            payload = json.loads(request.httprequest.data)

            if not self._verify_token(payload.get('token')):
                return {'status': 'error', 'message': 'Unauthorized'}

            fee_ref = payload.get('fee_ref')
            status = payload.get('status')

            fee = request.env['school.fee'].sudo().search([('name', '=', fee_ref)], limit=1)
            if not fee:
                return {'status': 'error', 'message': f'Fee {fee_ref} not found'}

            if status == 'paid':
                fee.action_pay()
                _logger.info(f"Fee {fee_ref} marked as paid via webhook")
                return {'status': 'ok', 'message': f'Fee {fee_ref} updated to paid'}

            return {'status': 'error', 'message': 'Unknown payment status'}

        except Exception as e:
            _logger.error(f"Payment webhook error: {str(e)}")
            return {'status': 'error', 'message': str(e)}


# ═══════════════════════════════════════════════════════════════
# PART 2 — OUTBOUND: Call external services FROM Odoo
# ═══════════════════════════════════════════════════════════════

class SchoolExternalService:
    """
    Service class for outbound API calls.
    Call from models or scheduled actions.
    """

    @staticmethod
    def _get_param(key):
        return http.request.env['ir.config_parameter'].sudo().get_param(key)

    @staticmethod
    def send_sms_to_parent(student, message):
        """
        Send SMS to parent via external SMS gateway.
        Usage: SchoolExternalService.send_sms_to_parent(student, "Your child was absent today.")
        """
        api_key = http.request.env['ir.config_parameter'].sudo().get_param(
            'school_system.sms_api_key'
        )
        if not api_key:
            _logger.warning("SMS API key not configured in Settings.")
            return False

        if not student.parent_phone:
            _logger.warning(f"No parent phone for student {student.name}")
            return False

        url = "https://api.smsgateway.com/v1/send"
        payload = {
            "api_key": api_key,
            "to": student.parent_phone,
            "message": message,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            _logger.info(f"SMS sent to {student.parent_phone}: {data}")
            return True
        except requests.exceptions.Timeout:
            _logger.error("SMS gateway timeout")
            return False
        except requests.exceptions.HTTPError as e:
            _logger.error(f"SMS gateway HTTP error: {e}")
            return False
        except Exception as e:
            _logger.error(f"SMS error: {str(e)}")
            return False

    @staticmethod
    def sync_student_to_external_db(student):
        """
        Push student data to an external Ministry/Government database.
        Called after student creation or update.
        """
        ICP = http.request.env['ir.config_parameter'].sudo()
        api_url = ICP.get_param('school_system.external_api_url')
        api_key = ICP.get_param('school_system.external_api_key')

        if not api_url or not api_key:
            _logger.warning("External API not configured.")
            return False

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "national_id": student.national_id,
            "name": student.name,
            "gender": student.gender,
            "date_of_birth": str(student.date_of_birth) if student.date_of_birth else None,
            "school_id_code": student.student_code,
        }

        try:
            response = requests.post(
                f"{api_url}/students/sync",
                json=payload,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            _logger.info(f"Student {student.student_code} synced to external DB.")
            return True
        except requests.exceptions.ConnectionError:
            _logger.error("Cannot reach external DB — connection error.")
            return False
        except requests.exceptions.HTTPError as e:
            _logger.error(f"External DB error: {e.response.status_code} — {e.response.text}")
            return False
        except Exception as e:
            _logger.error(f"Unexpected sync error: {str(e)}")
            return False

    @staticmethod
    def notify_absent_parents(date=None):
        """
        Cron-called method: find all absent students today and SMS their parents.
        Add to cron: SchoolExternalService.notify_absent_parents()
        """
        from odoo.fields import Date
        target_date = date or Date.today()
        absent = http.request.env['school.attendance'].sudo().search([
            ('date', '=', target_date),
            ('state', '=', 'absent'),
        ])
        for att in absent:
            msg = (
                f"Dear {att.student_id.parent_name}, "
                f"your child {att.student_id.name} was absent on {target_date}. "
                f"Please contact the school for more information."
            )
            SchoolExternalService.send_sms_to_parent(att.student_id, msg)

        _logger.info(f"Absence notifications sent for {len(absent)} students on {target_date}")
