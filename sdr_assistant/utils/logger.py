"""
Logging configuration for the SDR Assistant application.
Provides consistent logging across all modules.
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def setup_logger(name, log_file='app.log', level=logging.INFO):
    """
    Set up a logger with console and file handlers.
    
    Args:
        name: Name of the logger
        log_file: File to log to
        level: Logging level
        
    Returns:
        Configured logger
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, log_file),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Add handlers if they don't exist
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# Application-wide logger
app_logger = setup_logger('sdr_assistant')
