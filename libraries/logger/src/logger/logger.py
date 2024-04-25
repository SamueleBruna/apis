import logging
import configparser
import os

from pathlib import Path


class Logger:
    """
     A logger class that reads configuration from an ini file and uses a StreamHandler.
    """

    def __init__(self, config_ini: Path = Path(__file__) / Path("../../../config/logging.ini")):
        """
        Initializes the logger with the specified configuration file.
        Right now its imposed the ini file!
        """
        self.config_file = config_ini
        self.logger = logging.getLogger(__name__)
        self.configure_logging()

    def configure_logging(self):
        """
        Reads configuration from the ini file and sets up a StreamHandler with formatter.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)

        # Read configuration options.
        # The fallback works when there is no ini.file
        log_level = config.get('LOGGING', 'level', fallback='INFO')
        formatter_fmt = config.get('LOGGING', 'formatter',
                                   fallback='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Set up logging level
        # It gets the attribute from the object (logging library) which corresponds to log_level.upper()
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Set up stream handler with formatter
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(formatter_fmt)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def debug(self, message):
        """
        Logs a debug message.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Logs an informational message.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Logs a warning message.
        """
        self.logger.warning(message)

    def exception(self, message):
        """
        Logs an error/exception message.
        """
        self.logger.exception(message)

    def error(self, message):
        """
        Logs an error message.
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Logs a critical message.
        """
        self.logger.critical(message)


# Example usage
if __name__ == '__main__':
    logger = Logger()
    logger.info('Application started')
    logger.warning('Potential issue detected')
    logger.exception('An exception occurred')
    logger.error('An error occurred')
    logger.critical('A critical error occurred')
