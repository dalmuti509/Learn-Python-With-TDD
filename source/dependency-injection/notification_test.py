import pytest
from notification import (NotificationService, EmailNotifier, SMSNotifier, PushNotifier,
                        NotificationFactory, RetryNotifier, LoggingNotifier)

class FailingNotifier:
    def send(self, recipient, message):
        return False

def test_notification_service_with_email():
    email_notifier = EmailNotifier()
    service = NotificationService(email_notifier)
    
    result = service.send_notification("user@example.com", "Hello World")
    assert result == True

def test_notification_service_with_sms():
    sms_notifier = SMSNotifier()
    service = NotificationService(sms_notifier)
    
    result = service.send_notification("+1234567890", "Hello World")
    assert result == True

def test_notification_service_with_push():
    push_notifier = PushNotifier()
    service = NotificationService(push_notifier)
    
    result = service.send_notification("device123", "Hello World")
    assert result == True

def test_notification_service_failure():
    failing_notifier = FailingNotifier()
    service = NotificationService(failing_notifier)
    
    result = service.send_notification("user@example.com", "Hello World")
    assert result == False

def test_notification_service_batch():
    email_notifier = EmailNotifier()
    service = NotificationService(email_notifier)
    
    notifications = [
        ("user1@example.com", "Message 1"),
        ("user2@example.com", "Message 2"),
        ("user3@example.com", "Message 3")
    ]
    
    results = service.send_batch_notifications(notifications)
    assert len(results) == 3
    assert all(results)

def test_notification_factory():
    factory = NotificationFactory()
    
    email_service = factory.create_email_service()
    assert isinstance(email_service.notifier, EmailNotifier)
    
    sms_service = factory.create_sms_service()
    assert isinstance(sms_service.notifier, SMSNotifier)

def test_notification_service_with_retry():
    failing_notifier = FailingNotifier()
    retry_notifier = RetryNotifier(failing_notifier, max_retries=3)
    service = NotificationService(retry_notifier)
    
    result = service.send_notification("user@example.com", "Hello World")
    assert result == True

def test_notification_service_with_logging():
    email_notifier = EmailNotifier()
    logging_notifier = LoggingNotifier(email_notifier)
    service = NotificationService(logging_notifier)
    
    result = service.send_notification("user@example.com", "Hello World")
    assert result == True

