import logging


class CustomLoggerClass:
    """Custom logger for logging"""
    def __init__(self):
        self.logger = logging.getLogger("custom_logger")
        self.logger.setLevel(logging.DEBUG)
        self.create_file_handler()

    def create_file_handler(self):
        """File handler to specify files for logging"""
        # Create a file handler
        file_handler = logging.FileHandler("custom.log")

        # Create a formatter and add it to the handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        return self.logger
