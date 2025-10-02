# Dependency Injection

Let's explore dependency injection in Python using TDD. We'll build a notification system that demonstrates how to decouple components and make code more testable and maintainable.

## The Problem

We want to create a notification system that can send messages through different channels (email, SMS, push notifications) without tightly coupling the notification logic to specific implementations.

## Red: Write Failing Tests

Let's start with some basic dependency injection tests:

```python
# notification_test.py
import pytest
from notification import NotificationService, EmailNotifier, SMSNotifier, PushNotifier

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

class FailingNotifier:
    def send(self, recipient, message):
        return False
```

## Green: Write the Minimal Code to Pass

Now let's implement our notification system:

```python
# notification.py
class NotificationService:
    """
    A notification service that uses dependency injection.
    """
    
    def __init__(self, notifier):
        """
        Initialize the notification service.
        
        Args:
            notifier: The notification implementation to use
        """
        self.notifier = notifier
    
    def send_notification(self, recipient, message):
        """
        Send a notification to a recipient.
        
        Args:
            recipient (str): The recipient's address
            message (str): The message to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.notifier.send(recipient, message)
    
    def send_batch_notifications(self, notifications):
        """
        Send multiple notifications.
        
        Args:
            notifications (list): List of (recipient, message) tuples
            
        Returns:
            list: List of success/failure results
        """
        results = []
        for recipient, message in notifications:
            result = self.send_notification(recipient, message)
            results.append(result)
        return results

class EmailNotifier:
    """
    Email notification implementation.
    """
    
    def send(self, recipient, message):
        """
        Send an email notification.
        
        Args:
            recipient (str): Email address
            message (str): Message content
            
        Returns:
            bool: True if successful
        """
        # Simulate email sending
        print(f"Email sent to {recipient}: {message}")
        return True

class SMSNotifier:
    """
    SMS notification implementation.
    """
    
    def send(self, recipient, message):
        """
        Send an SMS notification.
        
        Args:
            recipient (str): Phone number
            message (str): Message content
            
        Returns:
            bool: True if successful
        """
        # Simulate SMS sending
        print(f"SMS sent to {recipient}: {message}")
        return True

class PushNotifier:
    """
    Push notification implementation.
    """
    
    def send(self, recipient, message):
        """
        Send a push notification.
        
        Args:
            recipient (str): Device ID
            message (str): Message content
            
        Returns:
            bool: True if successful
        """
        # Simulate push notification
        print(f"Push notification sent to {recipient}: {message}")
        return True
```

## Run the Tests

```bash
pytest notification_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and more sophisticated features:

```python
# notification.py
from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Notifier(ABC):
    """
    Abstract base class for notification implementations.
    """
    
    @abstractmethod
    def send(self, recipient, message):
        """
        Send a notification.
        
        Args:
            recipient (str): The recipient's address
            message (str): The message to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def validate_recipient(self, recipient):
        """
        Validate the recipient format.
        
        Args:
            recipient (str): The recipient to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return bool(recipient and recipient.strip())

class NotificationService:
    """
    A notification service that uses dependency injection.
    """
    
    def __init__(self, notifier):
        """
        Initialize the notification service.
        
        Args:
            notifier (Notifier): The notification implementation to use
        """
        if not isinstance(notifier, Notifier):
            raise TypeError("Notifier must implement the Notifier interface")
        self.notifier = notifier
    
    def send_notification(self, recipient, message):
        """
        Send a notification to a recipient.
        
        Args:
            recipient (str): The recipient's address
            message (str): The message to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.notifier.validate_recipient(recipient):
            logger.error(f"Invalid recipient: {recipient}")
            return False
        
        if not message or not message.strip():
            logger.error("Empty message")
            return False
        
        try:
            result = self.notifier.send(recipient, message)
            if result:
                logger.info(f"Notification sent successfully to {recipient}")
            else:
                logger.error(f"Failed to send notification to {recipient}")
            return result
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False
    
    def send_batch_notifications(self, notifications):
        """
        Send multiple notifications.
        
        Args:
            notifications (list): List of (recipient, message) tuples
            
        Returns:
            list: List of success/failure results
        """
        results = []
        for recipient, message in notifications:
            result = self.send_notification(recipient, message)
            results.append(result)
        return results

class EmailNotifier(Notifier):
    """
    Email notification implementation.
    """
    
    def send(self, recipient, message):
        """
        Send an email notification.
        
        Args:
            recipient (str): Email address
            message (str): Message content
            
        Returns:
            bool: True if successful
        """
        # Simulate email sending
        print(f"Email sent to {recipient}: {message}")
        return True
    
    def validate_recipient(self, recipient):
        """
        Validate email address format.
        
        Args:
            recipient (str): Email address to validate
            
        Returns:
            bool: True if valid email format
        """
        if not super().validate_recipient(recipient):
            return False
        return "@" in recipient and "." in recipient

class SMSNotifier(Notifier):
    """
    SMS notification implementation.
    """
    
    def send(self, recipient, message):
        """
        Send an SMS notification.
        
        Args:
            recipient (str): Phone number
            message (str): Message content
            
        Returns:
            bool: True if successful
        """
        # Simulate SMS sending
        print(f"SMS sent to {recipient}: {message}")
        return True
    
    def validate_recipient(self, recipient):
        """
        Validate phone number format.
        
        Args:
            recipient (str): Phone number to validate
            
        Returns:
            bool: True if valid phone format
        """
        if not super().validate_recipient(recipient):
            return False
        return recipient.startswith("+") and len(recipient) >= 10

class PushNotifier(Notifier):
    """
    Push notification implementation.
    """
    
    def send(self, recipient, message):
        """
        Send a push notification.
        
        Args:
            recipient (str): Device ID
            message (str): Message content
            
        Returns:
            bool: True if successful
        """
        # Simulate push notification
        print(f"Push notification sent to {recipient}: {message}")
        return True
    
    def validate_recipient(self, recipient):
        """
        Validate device ID format.
        
        Args:
            recipient (str): Device ID to validate
            
        Returns:
            bool: True if valid device ID
        """
        if not super().validate_recipient(recipient):
            return False
        return len(recipient) >= 5
```

## Advanced Examples

Let's add some more sophisticated dependency injection patterns:

```python
# notification_test.py (additional tests)
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

class FailingNotifier(Notifier):
    def send(self, recipient, message):
        return False

class RetryNotifier(Notifier):
    def __init__(self, notifier, max_retries=3):
        self.notifier = notifier
        self.max_retries = max_retries
    
    def send(self, recipient, message):
        for attempt in range(self.max_retries):
            if self.notifier.send(recipient, message):
                return True
        return False

class LoggingNotifier(Notifier):
    def __init__(self, notifier):
        self.notifier = notifier
    
    def send(self, recipient, message):
        logger.info(f"Attempting to send notification to {recipient}")
        result = self.notifier.send(recipient, message)
        logger.info(f"Notification result: {result}")
        return result
```

```python
# notification.py (additional classes)
class NotificationFactory:
    """
    Factory for creating notification services.
    """
    
    def create_email_service(self):
        """
        Create an email notification service.
        
        Returns:
            NotificationService: Email notification service
        """
        return NotificationService(EmailNotifier())
    
    def create_sms_service(self):
        """
        Create an SMS notification service.
        
        Returns:
            NotificationService: SMS notification service
        """
        return NotificationService(SMSNotifier())
    
    def create_push_service(self):
        """
        Create a push notification service.
        
        Returns:
            NotificationService: Push notification service
        """
        return NotificationService(PushNotifier())
    
    def create_service_with_retry(self, notifier, max_retries=3):
        """
        Create a notification service with retry logic.
        
        Args:
            notifier (Notifier): Base notifier
            max_retries (int): Maximum number of retries
            
        Returns:
            NotificationService: Notification service with retry
        """
        retry_notifier = RetryNotifier(notifier, max_retries)
        return NotificationService(retry_notifier)
    
    def create_service_with_logging(self, notifier):
        """
        Create a notification service with logging.
        
        Args:
            notifier (Notifier): Base notifier
            
        Returns:
            NotificationService: Notification service with logging
        """
        logging_notifier = LoggingNotifier(notifier)
        return NotificationService(logging_notifier)
```

## What We've Learned

1. **Dependency Injection**: Passing dependencies to classes instead of creating them internally
2. **Interface Segregation**: Using abstract base classes to define contracts
3. **Factory Pattern**: Creating objects through factory methods
4. **Decorator Pattern**: Wrapping notifiers with additional functionality
5. **Testability**: Making code easier to test by injecting dependencies

## Exercises

1. Add a method to send notifications to multiple channels
2. Implement a notification service that can send to multiple recipients
3. Add support for notification templates
4. Create a notification service that can send to different channels based on recipient type

## Key Concepts

- **Dependency Injection**: Inverting control of object creation
- **Interface Segregation**: Defining clear contracts between components
- **Factory Pattern**: Centralizing object creation logic
- **Decorator Pattern**: Adding functionality without modifying existing code
- **Testability**: Making code easier to test and maintain

