# import boto3
# from django.core.mail.backends.base import BaseEmailBackend
# from django.conf import settings


# class SESBackend(BaseEmailBackend):
#     def __init__(self, fail_silently=False, **kwargs):
#         super().__init__(fail_silently=fail_silently)
#         self.client = boto3.client(
#             'ses',
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             region_name=settings.AWS_SES_REGION_NAME
#         )

#     def send_messages(self, email_messages):
#         sent_count = 0
#         for message in email_messages:
#             try:
#                 self.client.send_raw_email(
#                     Source=message.from_email,
#                     Destinations=message.recipients(),
#                     RawMessage={'Data': message.message().as_string()}
#                 )
#                 sent_count += 1
#             except Exception as e:
#                 if not self.fail_silently:
#                     raise e
#         return sent_count
