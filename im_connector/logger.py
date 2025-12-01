"""Logger modules."""

import logging

from im_connector.config import Settings


def get_logger(settings: Settings) -> logging.Logger:
    """Create and configure a logger for the orchestrator API service.

    The logger outputs log messages to the console with a detailed format including
    timestamp, log level, logger name, process and thread information, and the message.
    The log level is set based on the application settings.

    Args:
        settings: The application settings instance containing the log level.

    Returns:
        logging.Logger: The configured logger instance.

    """
    logger = logging.getLogger("orchestrator-im-connector")
    logger.setLevel(level=settings.LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s "
            "[%(processName)s: %(process)d - %(threadName)s: %(thread)d] "
            "%(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.propagate = False
    return logger
