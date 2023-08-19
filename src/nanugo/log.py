import logging


def setup_logger(level=logging.INFO):
    """Sets up logger. You don't want to change this unless needed."""
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = setup_logger()  # import this `logger` created instead of setup_logger() itself
