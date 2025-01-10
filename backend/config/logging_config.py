import logging
import os
from logging.config import dictConfig

def setup_logging():
    """
    Configures logging settings for the entire application.
    """
    log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
    log_dir = os.getenv('LOG_DIR', 'logs')

    # Ensure log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'simple': {
                'format': '%(levelname)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': log_level
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detailed',
                'level': log_level,
                'filename': os.path.join(log_dir, 'app.log'),
                'maxBytes': 10485760,  # 10 MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detailed',
                'level': 'ERROR',
                'filename': os.path.join(log_dir, 'error.log'),
                'maxBytes': 10485760,
                'backupCount': 3
            }
        },
        'root': {
            'level': log_level,
            'handlers': ['console', 'file', 'error_file']
        },
        'loggers': {
            'flask_app': {  # Logger for Flask app
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    })
