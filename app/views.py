from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from mailjet_rest import Client
import json
import os


@require_http_methods(["POST"])
@csrf_exempt
def send_email(request):
    try:
        data = json.loads(request.body)

        subject = data.get('subject')
        message = data.get('message')
        recipient_list = data.get('recipients', [])
        from_email = data.get(
            'from_email', os.environ.get('MAILJET_SENDER_EMAIL'))
        html_message = data.get('html_message', message)

        if not all([subject, message, recipient_list]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        mailjet = Client(
            auth=(
                os.environ.get('MAILJET_API_KEY'),
                os.environ.get('MAILJET_SECRET_KEY'),
            ),
            version='v3.1'
        )

        email_data = {
            'Messages': [
                {
                    'From': {
                        'Email': from_email,
                        'Name': 'Attention Website Lead'
                    },
                    'To': [{'Email': recipient} for recipient in recipient_list],
                    'Subject': subject,
                    'TextPart': message,
                    'HTMLPart': html_message
                }
            ]
        }

        result = mailjet.send.create(data=email_data)

        if result.status_code == 200:
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to send email'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
