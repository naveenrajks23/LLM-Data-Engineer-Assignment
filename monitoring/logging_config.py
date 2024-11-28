import logging
import logging.config

def setup_logging(default_level=logging.INFO):
    """
    Set up the logging configuration.
    :param default_level: Default logging level, defaults to INFO.
    """
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(lineno)d'
            },
        },
        'handlers': {
            'console': {
                'level': default_level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'file': {
                'level': default_level,
                'class': 'logging.FileHandler',
                'filename': 'project_log.log',  # This file will store logs
                'formatter': 'detailed',
            },
        },
        'loggers': {
            '': {
                'level': default_level,
                'handlers': ['console', 'file'],
                'propagate': True,
            },
        },
    }
    
    logging.config.dictConfig(logging_config)
    logging.info("Logging setup complete.")

