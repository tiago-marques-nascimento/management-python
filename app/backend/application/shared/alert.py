from enum import Enum

class AlertType(Enum):
    SUCCESS = 1
    WARNING = 2
    ERROR = 3

class Alert():
    def __init__(self, alertType, alertMessage):
        self.alertTypeClass = 'alert-success' if alertType == AlertType.SUCCESS else 'alert-warning' if alertType == AlertType.WARNING else 'alert-error'
        self.alertTypeDescription = 'Success' if alertType == AlertType.SUCCESS else 'Warning' if alertType == AlertType.WARNING else 'Error'
        self.alertMessage = alertMessage
