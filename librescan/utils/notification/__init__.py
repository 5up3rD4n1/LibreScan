# Note: Import another notification service here if not running LS as web server
# Because by now the only mode is web server then WebSocket will be default
from .impl.web_socket_notification import WebSocketNotification as NotificationManager
