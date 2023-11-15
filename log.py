
import logging
logger = logging.getLogger('scanner_logger')
logger.setLevel(logging.DEBUG)
# Create a file handler
handler = logging.FileHandler('scanner.log')
handler.setLevel(logging.DEBUG)
# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)

def log_event(event_type, event_message):
    # Create a logger object
    
    # Log the event
    if event_type == 'info':
        logger.info(event_message)
    elif event_type == 'warning':
        logger.warning(event_message)
    elif event_type == 'error':
        logger.error(event_message)
    elif event_type == 'critical':
        logger.critical(event_message)
    else:
        logger.debug(event_message)

